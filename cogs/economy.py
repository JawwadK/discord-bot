import discord
from discord.ext import commands
import json
import random
from datetime import datetime, timedelta


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bank_data = {}
        self.load_bank_data()
        self.currency_name = "coins"
        self.daily_amount = 100
        self.work_cooldown = {}
        self.work_min = 10
        self.work_max = 100
        self.slots_min = 50

    def load_bank_data(self):
        try:
            with open('bank_data.json', 'r') as f:
                self.bank_data = json.load(f)
        except FileNotFoundError:
            self.bank_data = {}

    def save_bank_data(self):
        with open('bank_data.json', 'w') as f:
            json.dump(self.bank_data, f, indent=4)

    def get_account(self, user_id):
        user_id = str(user_id)
        if user_id not in self.bank_data:
            self.bank_data[user_id] = {
                "wallet": 0,
                "bank": 0,
                "bank_capacity": 1000,
                "last_daily": None
            }
            self.save_bank_data()
        return self.bank_data[user_id]

    @commands.command(name="balance", aliases=["bal"])
    async def balance(self, ctx, member: discord.Member = None):
        """Check your or someone else's balance"""
        user = member or ctx.author
        account = self.get_account(user.id)

        embed = discord.Embed(
            title=f"💰 {user.name}'s Balance", color=discord.Color.gold())
        embed.add_field(name="👛 Wallet",
                        value=f"{account['wallet']} {self.currency_name}")
        embed.add_field(
            name="🏦 Bank", value=f"{account['bank']}/{account['bank_capacity']} {self.currency_name}")
        await ctx.send(embed=embed)

    @commands.command()
    async def daily(self, ctx):
        """Claim your daily reward"""
        user_id = str(ctx.author.id)
        account = self.get_account(user_id)

        last_daily = account.get('last_daily')
        if last_daily:
            last_daily = datetime.fromisoformat(last_daily)
            if datetime.utcnow() - last_daily < timedelta(days=1):
                time_left = timedelta(days=1) - \
                    (datetime.utcnow() - last_daily)
                hours, remainder = divmod(time_left.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                await ctx.send(f"❌ You can claim your daily reward in {hours}h {minutes}m")
                return

        account['wallet'] += self.daily_amount
        account['last_daily'] = datetime.utcnow().isoformat()
        self.save_bank_data()

        embed = discord.Embed(
            title="✅ Daily Reward Claimed!",
            description=f"You received {self.daily_amount} {self.currency_name}!",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)  # 1 hour cooldown
    async def work(self, ctx):
        """Work to earn some coins"""
        earnings = random.randint(self.work_min, self.work_max)
        account = self.get_account(ctx.author.id)
        account['wallet'] += earnings
        self.save_bank_data()

        responses = [
            f"You worked as a developer and earned {earnings} {self.currency_name}!",
            f"You helped moderate a Discord server and earned {earnings} {self.currency_name}!",
            f"You fixed a bug and earned {earnings} {self.currency_name}!",
            f"You wrote some documentation and earned {earnings} {self.currency_name}!"
        ]

        embed = discord.Embed(
            title="💼 Work Complete!",
            description=random.choice(responses),
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            # Calculate remaining time
            remaining_time = int(error.retry_after)
            minutes, seconds = divmod(remaining_time, 60)
            hours, minutes = divmod(minutes, 60)

            # Create time string
            time_parts = []
            if hours > 0:
                time_parts.append(f"{hours}h")
            if minutes > 0:
                time_parts.append(f"{minutes}m")
            if seconds > 0:
                time_parts.append(f"{seconds}s")

            time_str = " ".join(time_parts)

            embed = discord.Embed(
                title="⏳ Work Cooldown",
                description=f"You're tired from your last job! Take a break and try again in **{time_str}**",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            # Prevent the error from propagating
            return
        # If it's a different type of error, let it propagate
        raise error

    @commands.command()
    async def deposit(self, ctx, amount: str):
        """Deposit money into your bank"""
        account = self.get_account(ctx.author.id)

        if amount.lower() == "all":
            amount = min(account['wallet'],
                         account['bank_capacity'] - account['bank'])
        else:
            try:
                amount = int(amount)
            except ValueError:
                await ctx.send("❌ Please enter a valid amount!")
                return

        if amount <= 0:
            await ctx.send("❌ Amount must be positive!")
            return
        if amount > account['wallet']:
            await ctx.send("❌ You don't have enough coins in your wallet!")
            return
        if account['bank'] + amount > account['bank_capacity']:
            await ctx.send("❌ Your bank is full!")
            return

        account['wallet'] -= amount
        account['bank'] += amount
        self.save_bank_data()

        embed = discord.Embed(
            title="🏦 Deposit Successful",
            description=f"Deposited {amount} {self.currency_name} into your bank!",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def withdraw(self, ctx, amount: str):
        """Withdraw money from your bank"""
        account = self.get_account(ctx.author.id)

        if amount.lower() == "all":
            amount = account['bank']
        else:
            try:
                amount = int(amount)
            except ValueError:
                await ctx.send("❌ Please enter a valid amount!")
                return

        if amount <= 0:
            await ctx.send("❌ Amount must be positive!")
            return
        if amount > account['bank']:
            await ctx.send("❌ You don't have enough coins in your bank!")
            return

        account['wallet'] += amount
        account['bank'] -= amount
        self.save_bank_data()

        embed = discord.Embed(
            title="🏦 Withdrawal Successful",
            description=f"Withdrew {amount} {self.currency_name} from your bank!",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def give(self, ctx, member: discord.Member, amount: int):
        """Give coins to another user"""
        if amount <= 0:
            await ctx.send("❌ Amount must be positive!")
            return
        if member.bot:
            await ctx.send("❌ You can't give coins to bots!")
            return
        if member == ctx.author:
            await ctx.send("❌ You can't give coins to yourself!")
            return

        account = self.get_account(ctx.author.id)
        if amount > account['wallet']:
            await ctx.send("❌ You don't have enough coins in your wallet!")
            return

        receiver_account = self.get_account(member.id)
        account['wallet'] -= amount
        receiver_account['wallet'] += amount
        self.save_bank_data()

        embed = discord.Embed(
            title="💸 Transfer Successful",
            description=f"Gave {amount} {self.currency_name} to {member.name}!",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def slots(self, ctx, amount: int):
        """Play the slot machine"""
        if amount < self.slots_min:
            await ctx.send(f"❌ Minimum bet is {self.slots_min} {self.currency_name}!")
            return

        account = self.get_account(ctx.author.id)
        if amount > account['wallet']:
            await ctx.send("❌ You don't have enough coins!")
            return

        symbols = ["🍎", "🍊", "🍇", "🍒", "💎", "7️⃣"]
        result = [random.choice(symbols) for _ in range(3)]

        # Calculate winnings
        winnings = 0
        if all(s == result[0] for s in result):  # All symbols match
            if result[0] == "7️⃣":
                winnings = amount * 10  # Jackpot
            elif result[0] == "💎":
                winnings = amount * 5
            else:
                winnings = amount * 3
        # Two matching symbols
        elif result.count(result[0]) == 2 or result.count(result[1]) == 2:
            winnings = amount * 1.5

        # Update balance
        account['wallet'] -= amount
        if winnings > 0:
            account['wallet'] += int(winnings)
        self.save_bank_data()

        # Create result message
        slot_display = " ".join(result)
        if winnings > 0:
            result_text = f"You won {int(winnings)} {self.currency_name}!"
            color = discord.Color.green()
        else:
            result_text = f"You lost {amount} {self.currency_name}!"
            color = discord.Color.red()

        embed = discord.Embed(title="🎰 Slots", color=color)
        embed.add_field(name="Result", value=slot_display, inline=False)
        embed.add_field(name="Outcome", value=result_text)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Economy(bot))
    print("Economy cog loaded")
