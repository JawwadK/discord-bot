import discord
from discord.ext import commands


class CustomHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.remove_command('help')  # Remove default help command

    def get_command_signature(self, command):
        """Get the command signature with parameters"""
        params = []
        for param in command.clean_params.values():
            if param.default == param.empty:
                params.append(f'<{param.name}>')
            else:
                params.append(f'[{param.name}]')

        return f"{self.bot.command_prefix}{command.name} {' '.join(params)}"

    @commands.command()
    async def help(self, ctx, command_name=None):
        """Shows help for all commands or specific command details"""
        if command_name:
            # Show detailed help for specific command
            command = self.bot.get_command(command_name)
            if command:
                embed = discord.Embed(
                    title=f"Command: {command.name}",
                    color=discord.Color.blue()
                )
                embed.add_field(
                    name="Usage",
                    value=f"`{self.get_command_signature(command)}`",
                    inline=False
                )
                if command.help:
                    embed.add_field(
                        name="Description",
                        value=command.help,
                        inline=False
                    )
                if command.aliases:
                    embed.add_field(
                        name="Aliases",
                        value=", ".join(command.aliases),
                        inline=False
                    )
                await ctx.send(embed=embed)
                return
            else:
                await ctx.send(f"❌ Command '{command_name}' not found.")
                return

        # Show all commands grouped by cog
        embed = discord.Embed(
            title="📚 Bot Commands",
            description=f"Use `{self.bot.command_prefix}help <command>` for detailed information about a command.",
            color=discord.Color.blue()
        )

        # Organize commands by cog
        for cog_name, cog in self.bot.cogs.items():
            # Skip the help command cog
            if cog_name == "CustomHelp":
                continue

            # Get all commands from the cog that the user can use
            commands_list = [
                f"`{self.bot.command_prefix}{cmd.name}`"
                for cmd in cog.get_commands()
                if not cmd.hidden
            ]

            if commands_list:
                # Add cog commands to embed
                embed.add_field(
                    name=f"{cog_name} Commands",
                    value=", ".join(commands_list),
                    inline=False
                )

        # Add footer with additional info
        embed.set_footer(
            text=f"Bot prefix: {self.bot.command_prefix} | Total Commands: {len(list(self.bot.commands)) - 1}"
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(CustomHelp(bot))
    print("Custom Help cog loaded")
