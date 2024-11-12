import discord
from discord.ext import commands
import json
import os
import asyncio
from datetime import datetime, timedelta
from src.utils.constants import REMINDERS_DATA_PATH, REMINDER_CHECK_INTERVAL


class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders = self.load_reminders()
        self.reminder_task = self.bot.loop.create_task(self.check_reminders())

    def load_reminders(self):
        try:
            with open(REMINDERS_DATA_PATH, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_reminders(self):
        with open(REMINDERS_DATA_PATH, 'w') as f:
            json.dump(self.reminders, f, indent=4)

    def parse_time(self, time_str):
        """Parse time string into seconds"""
        try:
            total_seconds = 0
            time_str = time_str.lower()

            # Parse years (new)
            if 'y' in time_str:
                years = int(time_str.split('y')[0])
                total_seconds += years * 365 * 86400  # Approximate year as 365 days
                time_str = time_str.split('y')[1]

            # Parse days
            if 'd' in time_str:
                days = int(time_str.split('d')[0])
                total_seconds += days * 86400
                time_str = time_str.split('d')[1]

            # Parse hours
            if 'h' in time_str:
                hours = int(time_str.split('h')[0])
                total_seconds += hours * 3600
                time_str = time_str.split('h')[1]

            # Parse minutes
            if 'm' in time_str:
                minutes = int(time_str.split('m')[0])
                total_seconds += minutes * 60

            if total_seconds == 0:
                raise ValueError

            return total_seconds
        except:
            raise ValueError("Invalid time format")

    def format_time_remaining(self, seconds):
        """Format seconds into readable time string"""
        years = seconds // (365 * 86400)  # Approximate year as 365 days
        remaining_seconds = seconds % (365 * 86400)
        days = remaining_seconds // 86400
        hours = (remaining_seconds % 86400) // 3600
        minutes = (remaining_seconds % 3600) // 60

        parts = []
        if years > 0:
            parts.append(f"{years}y")
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")

        return " ".join(parts) if parts else "Less than 1m"

    async def check_reminders(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            current_time = datetime.utcnow()
            due_reminders = []
            user_ids = list(self.reminders.keys())

            for user_id in user_ids:
                user_reminders = self.reminders[user_id]
                remaining_reminders = []

                for reminder in user_reminders:
                    reminder_time = datetime.fromisoformat(reminder['time'])

                    if reminder_time <= current_time:
                        due_reminders.append((user_id, reminder))

                        if reminder.get('repeat_interval'):
                            next_time = reminder_time + \
                                timedelta(seconds=reminder['repeat_interval'])
                            reminder['time'] = next_time.isoformat()
                            remaining_reminders.append(reminder)
                    else:
                        remaining_reminders.append(reminder)

                if remaining_reminders:
                    self.reminders[user_id] = remaining_reminders
                else:
                    del self.reminders[user_id]

            if due_reminders:
                self.save_reminders()
                for user_id, reminder in due_reminders:
                    try:
                        user = await self.bot.fetch_user(int(user_id))
                        if user:
                            # Create reminder notification embed
                            embed = discord.Embed(
                                title="🔔 Reminder",
                                description=reminder['message'],
                                color=discord.Color.blue()
                            )
                            if reminder.get('repeat_interval'):
                                next_time = datetime.fromisoformat(
                                    reminder['time'])
                                time_until_next = self.format_time_remaining(
                                    reminder['repeat_interval'])
                                embed.add_field(
                                    name="Next Reminder",
                                    value=f"Will remind again in {time_until_next}"
                                )
                            await user.send(embed=embed)
                    except discord.NotFound:
                        continue
                    except Exception as e:
                        print(f"Error sending reminder: {e}")

            await asyncio.sleep(60)

    def cog_unload(self):
        self.reminder_task.cancel()

    @commands.group(invoke_without_command=True)
    async def remind(self, ctx):
        """Shows remind command help"""
        embed = discord.Embed(
            title="📝 Reminder Commands",
            description="Here are all available reminder commands:",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="!remind me <time> <reminder>",
            value="Set a one-time reminder\nExample: !remind me 1h30m Take a break",
            inline=False
        )
        embed.add_field(
            name="!remind repeat <interval> <reminder>",
            value="Set a repeating reminder\nExample: !remind repeat 2h Drink water",
            inline=False
        )
        embed.add_field(
            name="!remind list",
            value="List all your active reminders",
            inline=False
        )
        embed.add_field(
            name="!remind clear",
            value="Clear all your reminders",
            inline=False
        )
        embed.add_field(
            name="Time Format",
            value="Use combinations of:\n"
                  "y = years (e.g., 1y)\n"
                  "d = days (e.g., 7d)\n"
                  "h = hours (e.g., 24h)\n"
                  "m = minutes (e.g., 30m)\n"
                  "Example: 1y6m, 5d12h, 1h30m",
            inline=False
        )

        await ctx.send(embed=embed)

    @remind.command(name="me")
    async def remind_me(self, ctx, time: str, *, reminder: str):
        """Set a one-time reminder"""
        try:
            total_seconds = self.parse_time(time)
            reminder_time = datetime.utcnow() + timedelta(seconds=total_seconds)
            user_id = str(ctx.author.id)

            if user_id not in self.reminders:
                self.reminders[user_id] = []

            self.reminders[user_id].append({
                'time': reminder_time.isoformat(),
                'message': reminder,
                'repeat_interval': None
            })

            self.save_reminders()

            embed = discord.Embed(
                title="✅ Reminder Set",
                description=reminder,
                color=discord.Color.green()
            )
            embed.add_field(
                name="Time Until Reminder",
                value=self.format_time_remaining(total_seconds),
                inline=False
            )
            embed.set_footer(text="Use !remind list to see all your reminders")

            await ctx.send(embed=embed)

        except ValueError:
            embed = discord.Embed(
                title="❌ Error",
                description="Invalid time format!",
                color=discord.Color.red()
            )
            embed.add_field(
                name="Correct Format",
                value="Use combinations of:\ny (years), d (days), h (hours), m (minutes)\n"
                      "Example: \n!Remind me 1y6m do something, \n!Remind me 5d12h do something else, \n!Remind me 1h30m do another thing",
                inline=False
            )
            await ctx.send(embed=embed)

    @remind.command(name="repeat")
    async def remind_repeat(self, ctx, interval: str, *, reminder: str):
        """Set a repeating reminder"""
        try:
            interval_seconds = self.parse_time(interval)
            reminder_time = datetime.utcnow() + timedelta(seconds=interval_seconds)
            user_id = str(ctx.author.id)

            if user_id not in self.reminders:
                self.reminders[user_id] = []

            self.reminders[user_id].append({
                'time': reminder_time.isoformat(),
                'message': reminder,
                'repeat_interval': interval_seconds
            })

            self.save_reminders()

            embed = discord.Embed(
                title="✅ Repeating Reminder Set",
                description=reminder,
                color=discord.Color.green()
            )
            embed.add_field(
                name="Repeat Interval",
                value=f"Will remind you every {self.format_time_remaining(interval_seconds)}",
                inline=False
            )
            embed.add_field(
                name="First Reminder",
                value=f"In {self.format_time_remaining(interval_seconds)}",
                inline=False
            )
            embed.set_footer(text="Use !remind list to see all your reminders")

            await ctx.send(embed=embed)

        except ValueError:
            embed = discord.Embed(
                title="❌ Error",
                description="Invalid time format!",
                color=discord.Color.red()
            )
            embed.add_field(
                name="Correct Format",
                value="Use combinations of:\ny (years), d (days), h (hours), m (minutes)\n"
                      "Example: 1y6m, 5d12h, 1h30m",
                inline=False
            )
            await ctx.send(embed=embed)

    @remind.command(name="list")
    async def list_reminders(self, ctx):
        """List all your active reminders"""
        user_id = str(ctx.author.id)
        if user_id not in self.reminders or not self.reminders[user_id]:
            embed = discord.Embed(
                title="📝 Your Reminders",
                description="You have no active reminders.",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="📝 Your Reminders",
            description=f"You have {len(self.reminders[user_id])} active reminder(s)",
            color=discord.Color.blue()
        )

        for i, reminder in enumerate(self.reminders[user_id], 1):
            reminder_time = datetime.fromisoformat(reminder['time'])
            time_left = (reminder_time - datetime.utcnow()).total_seconds()

            if reminder.get('repeat_interval'):
                interval_str = self.format_time_remaining(
                    reminder['repeat_interval'])
                reminder_type = f"⭐ Repeating (every {interval_str})"
            else:
                reminder_type = "🕐 One-time"

            embed.add_field(
                name=f"Reminder #{i}",
                value=f"📌 {reminder['message']}\n"
                f"📋 Type: {reminder_type}\n"
                f"⏳ Next reminder in: {self.format_time_remaining(int(time_left))}",
                inline=False
            )

        embed.set_footer(text="Use !remind clear to clear all reminders")
        await ctx.send(embed=embed)

    @remind.command(name="clear")
    async def clear_reminders(self, ctx):
        """Clear all your reminders"""
        user_id = str(ctx.author.id)
        if user_id in self.reminders:
            reminder_count = len(self.reminders[user_id])
            del self.reminders[user_id]
            self.save_reminders()

            embed = discord.Embed(
                title="✅ Reminders Cleared",
                description=f"Successfully cleared {reminder_count} reminder(s)",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="❌ No Reminders",
                description="You have no reminders to clear",
                color=discord.Color.red()
            )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Reminders(bot))
    print("Reminders cog loaded")
