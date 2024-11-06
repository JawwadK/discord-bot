import discord
from discord.ext import commands
import requests
import random


class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def greet(self, ctx):
        await ctx.send('Hello from MyCog!')

    @commands.command()
    async def ping(self, ctx):  # Added self here
        await ctx.send('Pong!')

    @commands.command()
    async def hello(self, ctx):  # Added self here
        await ctx.send(f'Hello, {ctx.author.name}!')

    @commands.command()
    async def wumbo(self, ctx):  # Added self here
        await ctx.send('WUMBO')

    @commands.command()
    async def info(self, ctx):  # Added self here
        embed = discord.Embed(
            title="Bot Info", description="This is a test bot", color=discord.Color.blue())
        embed.add_field(name="Creator", value="Jawwad")
        embed.add_field(name="Language", value="Python")
        await ctx.send(embed=embed)

    @commands.command()
    async def meme(self, ctx):
        response = requests.get('https://meme-api.com/gimme')
        if response.status_code == 200:
            meme_data = response.json()
            await ctx.send(meme_data['url'])
        else:
            await ctx.send('Failed to retrieve meme:', response.status_code)

    @commands.command()
    async def eightball(self, ctx, *, question):
        responses = ["Yes", "No", "Maybe", "Ask again later",
                     "Definitely", "Absolutely not", "I wouldn't count on it", "Dumbass (Roll Again)"
                     ]
        await ctx.send(f'🎱{random.choice(responses)}')

    @commands.command()
    async def cat(self, ctx):
        response = requests.get('https://api.thecatapi.com/v1/images/search')
        if response.status_code == 200:
            cat_data = response.json()
        else:
            await ctx.send('Could not fetch a cat picture. Try again later!')

    @commands.command()
    async def flipcoin(self, ctx):
        result = random.choice(['Heads', 'Tails'])
        await ctx.send(f'🪙 The coin landed on {result}!')

    @commands.command()
    async def rolldice(self, ctx, sides: int = 6):
        result = random.random.randint(1, sides)
        await ctx.send(f'You rolled a {result}')

    @commands.command()
    async def quotes(self, ctx):
        quotes = [
            "These dudes think they the shit, they haven't even farted yet",
            "honestly im not gay but if some man that was hella stacked could sceure me for the rest of my life i thihnk i'd be fine with being gay - Kingsley Lam",
            "Holy shit my cheeks are fking destroyed - Darren Chen",
            "Actually looks Like a girl \n Hot girl too \n Smashable - Jay Modi",
        ]
        quote = random.choice(quotes)
        await ctx.send(f'This was said by someone in the server once: "{quote}"')
    
    @commands.command()
    async def trivia(self, ctx):
        questions = {
            "What is Jacky Ly Chinese Name" : "Legume Singh",
            "Whats Steph real name" : "Weenig",
            "Whats 9 + 10" : "21"
        }
        question, answer = random.choice(list(questions.items()))
        await ctx.send(f'Trivia Questions: {question}')
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            answer_msg = await self.bot.wait_for('message', check=check, timeout=30)
            if answer_msg.content.lower == answer.lower():
                await ctx.send('Correct!')
            else:
                await ctx.send(f'Wrong!')
        except asyncio.TimeoutError:
            await ctx.send(f'Time\'s up!')

    @commands.command()
    async def joke(self, ctx):
        response = requests.get('https://official-joke-api.appspot.com/random_joke')
        if response.status_code == 200:
            joke = response.json()
            await ctx.send(f'{joke["setup"]} - {joke["punchline"]}')
        else:
            await ctx.send('Could not fetch a joke. Try again later!')



async def setup(bot):
    await bot.add_cog(MyCog(bot))
    print("MyCog loaded")
