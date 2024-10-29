import discord
from discord.ext import commands
import json
import os
import asyncio
from datetime import datetime, timedelta

REMINDERS_FILE = 'reminders.json'

class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load_reminders(self):
        if os.path.exists(REMINDERS_FILE):
            with open(REMINDERS_FILE, 'r') as f:
                return json.load(f)
        return {}


    def save_reminders(self):
        with open(REMINDERS_FILE, 'w') as f:
            json.dump(self.reminders, f)

    async def check_reminders(self):
        await self.bot.wait_until_ready()
        while self.bot.is_closed():
            current_time = datetime.utcnow()
            due_reminders = []

        for user_id, user_reminders in self.reminders.items():
                        for reminder in user_reminders:
                            if datetime.fromisoformat(reminder['time']) <= current_time:
                                due_reminders.append((user_id, reminder['message']))
                                user_reminders.remove(reminder)

                        if not user_reminders:
                            del self.reminders[user_id]

                    self.save_reminders()

                    for user_id, message in due_reminders:
                        user = self.bot.get_user(int(user_id))
                        if user:
                            await user.send(f'🚨 Reminder: {message}')

                    await asyncio.sleep(60)


"""             for user_id, user_reminders in self.reminders.items():
                for reminder in user_reminders:
                    if datetime.fromisoformat(reminder['time']) <= current_time:
                        due_reminders.append((user_id, reminder['message'])) """


"""     @commands.command()
    async def remind(self, ctx, seconds: int, *, reminder: str):
        user_id = str(ctx.author.id)
        reminder_time = datetime.utcnow() + timedelta(seconds=seconds)

        if user_id not in self.reminders:
            self.reminders[user_id] = []
        self.reminders[user_id].append({'time': reminder_time.isoformat(), 'message': reminder})
        
        self.save_reminders()
        await ctx.send(f'Reminder set for {seconds} seconds: "{reminder}"')
    @commands.command()
 """
def setup(bot):
    bot.add_cog(Reminders(bot))