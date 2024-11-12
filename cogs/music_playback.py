import discord
from discord.ext import commands
import yt_dlp  # Changed from youtube_dl to yt_dlp
import asyncio
from async_timeout import timeout
import itertools

ytdl_format_options = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
}

# Using yt_dlp instead of youtube_dl
ytdl = yt_dlp.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        # Changed to handle both URL types
        self.url = data.get('webpage_url', data.get('url'))
        self.duration = data.get('duration')

    @classmethod
    async def from_url(cls, url, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        if 'entries' in data:
            data = data['entries'][0]

        # Get the direct audio URL
        filename = data['url']
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class MusicPlayer:
    def __init__(self, ctx):
        self.bot = ctx.bot
        self.guild = ctx.guild
        self.channel = ctx.channel
        self.cog = ctx.cog
        self.queue = asyncio.Queue()
        self.next = asyncio.Event()
        self.current = None
        self.np = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                async with timeout(300):  # 5 minute timeout
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self.guild)

            if not isinstance(source, YTDLSource):
                try:
                    source = await YTDLSource.from_url(source, loop=self.bot.loop)
                except Exception as e:
                    await self.channel.send(f'An error occurred while processing your song.\n'
                                            f'```css\n[{e}]\n```')
                    continue

            source.volume = 0.5
            self.current = source

            self.guild.voice_client.play(
                source,
                after=lambda _: self.bot.loop.call_soon_threadsafe(
                    self.next.set)
            )

            embed = discord.Embed(
                title="Now playing",
                description=f"[{source.title}]({source.url})",
                color=discord.Color.green()
            )
            if source.duration:
                minutes = source.duration // 60
                seconds = source.duration % 60
                embed.add_field(name="Duration",
                                value=f"{minutes}:{seconds:02d}")

            self.np = await self.channel.send(embed=embed)
            await self.next.wait()
            self.current = None

    def destroy(self, guild):
        return self.bot.loop.create_task(self.cog.cleanup(guild))


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    def get_player(self, ctx):
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player
        return player

    @commands.command(name='join')
    async def join(self, ctx):
        """Joins your voice channel"""
        if ctx.author.voice is None:
            return await ctx.send("You're not connected to a voice channel.")

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(ctx.author.voice.channel)

        await ctx.author.voice.channel.connect()
        await ctx.send(f"Joined {ctx.author.voice.channel.name}!")

    @commands.command(name='play')
    async def play(self, ctx, *, url):
        """Plays audio from a YouTube URL"""
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                return await ctx.send("You're not connected to a voice channel.")

        async with ctx.typing():
            try:
                player = self.get_player(ctx)
                await player.queue.put(url)

                if not ctx.voice_client.is_playing():
                    await ctx.send(f"Adding to queue and playing now...")
                else:
                    await ctx.send(f"Added to queue!")
            except Exception as e:
                await ctx.send(f"An error occurred: {str(e)}")

    @commands.command(name='pause')
    async def pause(self, ctx):
        """Pauses the currently playing song"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Paused ⏸️")
        else:
            await ctx.send("Nothing is playing right now.")

    @commands.command(name='resume')
    async def resume(self, ctx):
        """Resumes the currently paused song"""
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Resumed ▶️")
        else:
            await ctx.send("Nothing is paused right now.")

    @commands.command(name='skip')
    async def skip(self, ctx):
        """Skips the current song"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Skipped ⏭️")
        else:
            await ctx.send("Nothing is playing right now.")

    @commands.command(name='queue')
    async def queue_info(self, ctx):
        """Shows the current queue"""
        player = self.get_player(ctx)

        if player.queue.empty():
            return await ctx.send('Queue is empty.')

        upcoming = list(itertools.islice(player.queue._queue, 0, 5))
        fmt = '\n'.join(f'**`{song}`**' for song in upcoming)
        embed = discord.Embed(
            title=f'Upcoming - Next {len(upcoming)}',
            description=fmt,
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command(name='leave', aliases=['disconnect'])
    async def leave(self, ctx):
        """Clears the queue and leaves the voice channel"""
        if ctx.voice_client is not None:
            await self.cleanup(ctx.guild)
            await ctx.send("Disconnected 👋")
        else:
            await ctx.send("I'm not connected to a voice channel.")


async def setup(bot):
    await bot.add_cog(Music(bot))
    print("Music cog loaded")
