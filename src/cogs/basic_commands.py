import discord
from discord.ext import commands
import requests
import random
import asyncio


class BasicCommands(commands.Cog):
    """Basic bot commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def greet(self, ctx):
        """Send a friendly greeting"""
        await ctx.send('Hello from the bot! 👋')

    @commands.command()
    async def ping(self, ctx):
        """Check if the bot is responsive"""
        await ctx.send('Pong! 🏓')

    @commands.command()
    async def hello(self, ctx):
        """Get a personalized hello message"""
        await ctx.send(f'Hello, {ctx.author.name}! 👋')

    @commands.command()
    async def wumbo(self, ctx):
        """I wumbo, you wumbo, he/she/we wumbo"""
        await ctx.send('WUMBO 🎉')

    @commands.command()
    async def info(self, ctx):
        """Get information about the bot"""
        embed = discord.Embed(
            title="Bot Info",
            description="This is a multi-purpose Discord bot",
            color=discord.Color.blue()
        )
        embed.add_field(name="Creator", value="Jawwad")
        embed.add_field(name="Language", value="Python")
        embed.add_field(name="Features",
                        value="Economy, Reminders, Fun Commands", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def meme(self, ctx):
        """Get a random meme"""
        try:
            response = requests.get('https://meme-api.com/gimme')
            if response.status_code == 200:
                meme_data = response.json()
                embed = discord.Embed(
                    title=meme_data['title'],
                    color=discord.Color.random()
                )
                embed.set_image(url=meme_data['url'])
                await ctx.send(embed=embed)
            else:
                await ctx.send('Failed to retrieve meme. Try again later! 😢')
        except Exception as e:
            await ctx.send('An error occurred while fetching the meme.')
            print(f"Error in meme command: {e}")

    @commands.command(name="8ball", aliases=["eightball"])
    async def eightball(self, ctx, *, question):
        """Ask the magic 8-ball a question"""
        responses = [
            "Yes", "No", "Maybe", "Ask again later",
            "Definitely", "Absolutely not", "I wouldn't count on it",
            "Dumbass (Roll Again)", "Without a doubt", "Better not tell you now",
            "My sources say no", "Outlook good", "Very doubtful"
        ]
        embed = discord.Embed(
            title="🎱 Magic 8-Ball",
            color=discord.Color.purple()
        )
        embed.add_field(name="Question", value=question, inline=False)
        embed.add_field(name="Answer", value=random.choice(
            responses), inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def cat(self, ctx):
        """Get a random cat picture"""
        try:
            response = requests.get(
                'https://api.thecatapi.com/v1/images/search')
            if response.status_code == 200:
                cat_data = response.json()
                embed = discord.Embed(
                    title="🐱 Random Cat",
                    color=discord.Color.orange()
                )
                embed.set_image(url=cat_data[0]['url'])
                await ctx.send(embed=embed)
            else:
                await ctx.send('Could not fetch a cat picture. Try again later! 😿')
        except Exception as e:
            await ctx.send('An error occurred while fetching the cat picture.')
            print(f"Error in cat command: {e}")

    @commands.command()
    async def flipcoin(self, ctx):
        """Flip a coin"""
        result = random.choice(['Heads', 'Tails'])
        embed = discord.Embed(
            title="🪙 Coin Flip",
            description=f"The coin landed on **{result}**!",
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def rolldice(self, ctx, sides: int = 6):
        """Roll a dice with specified number of sides"""
        if sides < 1:
            await ctx.send("The dice must have at least 1 side! 🎲")
            return
        result = random.randint(1, sides)
        embed = discord.Embed(
            title="🎲 Dice Roll",
            description=f"Rolling a {sides}-sided dice...\nYou rolled a **{result}**!",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def quote(self, ctx):
        """Get a random quote from server members"""
        quotes = [
            "These dudes think they the shit, they haven't even farted yet",
            "honestly im not gay but if some man that was hella stacked could sceure me for the rest of my life i thihnk i'd be fine with being gay - Kingsley Lam",
            "Holy shit my cheeks are fking destroyed - Darren Chen",
            "Actually looks Like a girl \n Hot girl too \n Smashable - Jay Modi",
        ]
        quote = random.choice(quotes)
        embed = discord.Embed(
            title="💭 Server Quote",
            description=f"*{quote}*",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def trivia(self, ctx):
        """Start a trivia question"""
        questions = {
            "What is Jacky Ly Chinese Name": "Legume Singh",
            "Whats Steph real name": "Wee nig",
            "Whats 9 + 10": "21"
        }
        question, answer = random.choice(list(questions.items()))
        embed = discord.Embed(
            title="❓ Trivia Time",
            description=f"**Question:** {question}",
            color=discord.Color.blue()
        )
        embed.set_footer(text="You have 30 seconds to answer!")
        await ctx.send(embed=embed)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            answer_msg = await self.bot.wait_for('message', check=check, timeout=30)
            if answer_msg.content.lower() == answer.lower():
                embed = discord.Embed(
                    title="✅ Correct!",
                    color=discord.Color.green()
                )
            else:
                embed = discord.Embed(
                    title="❌ Wrong!",
                    description=f"The correct answer was: **{answer}**",
                    color=discord.Color.red()
                )
            await ctx.send(embed=embed)
        except asyncio.TimeoutError:
            await ctx.send('⏰ Time\'s up!')

    @commands.command()
    async def joke(self, ctx):
        """Get a random joke"""
        try:
            response = requests.get(
                'https://official-joke-api.appspot.com/random_joke')
            if response.status_code == 200:
                joke = response.json()
                embed = discord.Embed(
                    title="😄 Random Joke",
                    color=discord.Color.green()
                )
                embed.add_field(
                    name="Setup", value=joke["setup"], inline=False)
                embed.add_field(name="Punchline",
                                value=joke["punchline"], inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send('Could not fetch a joke. Try again later! 😢')
        except Exception as e:
            await ctx.send('An error occurred while fetching the joke.')
            print(f"Error in joke command: {e}")

    # Error handling for the commands
    @eightball.error
    async def eightball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ You need to ask a question! Try: `!8ball Will I win the lottery?`")

    @rolldice.error
    async def rolldice_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("❌ Please provide a valid number of sides! Example: `!rolldice 20`")


async def setup(bot):
    await bot.add_cog(BasicCommands(bot))
    print("Basic Commands cog loaded")
