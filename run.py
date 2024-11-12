import asyncio
from src.bot import DiscordBot
from config.config import TOKEN


async def main():
    bot = DiscordBot()
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
