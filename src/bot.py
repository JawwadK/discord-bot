import discord
from discord.ext import commands
import os
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    filename='logs/bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('discord_bot')


class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        # Create necessary directories if they don't exist
        os.makedirs('data/bank', exist_ok=True)
        os.makedirs('data/reminders', exist_ok=True)
        os.makedirs('logs', exist_ok=True)

        # Load all cogs
        for filename in os.listdir('./src/cogs'):
            if filename.endswith('.py') and filename != '__init__.py':
                try:
                    await self.load_extension(f'src.cogs.{filename[:-3]}')
                    logger.info(f'Loaded cog: {filename[:-3]}')
                except Exception as e:
                    logger.error(
                        f'Failed to load cog {filename[:-3]}: {str(e)}')

    async def on_ready(self):
        logger.info(f'Bot is online as {self.user}')
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="!help for commands"
            )
        )

    async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)

        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ Command not found! Use !help to see available commands.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command!")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Missing required argument! Check !help [command] for proper usage.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Invalid argument provided! Check !help [command] for proper usage.")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("❌ This command cannot be used in private messages!")
        elif isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            await ctx.send(f"❌ Command is on cooldown! Try again in {int(minutes)}m {int(seconds)}s")
        else:
            logger.error(f'Unexpected error in {ctx.command}: {str(error)}')
            await ctx.send("❌ An unexpected error occurred while executing the command.")
