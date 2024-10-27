import discord
from discord.ext import commands
from config import TOKEN
import requests

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')


async def main():
    async with bot:
        await bot.load_extension('my_cog')
        await bot.start(TOKEN)

# Start the bot
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
