import discord
from discord.ext import commands
import os
from config import TOKEN


class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        # Load all cogs from the cogs directory
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and filename != '__init__.py':
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f'Loaded cog: {filename[:-3]}')
                except Exception as e:
                    print(f'Failed to load cog {filename[:-3]}: {str(e)}')

    async def on_ready(self):
        print(f'Bot is online as {self.user}')
        # Set a status for the bot
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="!help for commands"
            )
        )

    async def on_command_error(self, ctx, error):
        # Unwrap the error if it's wrapped in CommandInvokeError
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
            # This shouldn't trigger anymore for the work command, but good to have as backup
            minutes, seconds = divmod(error.retry_after, 60)
            await ctx.send(f"❌ Command is on cooldown! Try again in {int(minutes)}m {int(seconds)}s")
        else:
            # Log unexpected errors
            print(f'Unexpected error in {ctx.command}: {str(error)}')
            await ctx.send("❌ An unexpected error occurred while executing the command.")


async def main():
    bot = DiscordBot()
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
