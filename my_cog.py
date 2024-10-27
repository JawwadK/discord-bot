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




async def setup(bot):
    await bot.add_cog(MyCog(bot))
    print("MyCog loaded")
