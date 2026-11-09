"""Core money commands."""

import random

import time
import discord
from discord import app_commands
from discord.ext import commands

import config
from utils import check_cooldown, fmt, parse_amount, fmt_duration


class Economy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    @app_commands.command(description="Check the bot is alive.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"🏓 Pong! {round(self.bot.latency * 1000)}ms")

# TODO: /balance [member]   - embed with wallet, bank, net worth
    @app_commands.command(description="Check your or another member's balance.")
    async def balance(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        wallet, bank = self.db.get_balance(member.id)
        total = wallet + bank
        if total > 1000:
            compliment = "💰 You're minted!"
        elif total < 100:
            compliment = "💸 You're skint mate!"
        else:
            compliment = "💵 Not bad, not bad."
        await interaction.response.send_message(
            f"{member.mention} has ${wallet} in their wallet 👛 and ${bank} in their bank 🏦, for a total of ${total}. {compliment}"
        )

# TODO: /daily              - DAILY_AMOUNT, 24h cooldown, plus bank interest (BANK_INTEREST_RATE)
    @app_commands.command(description="Don't claim this, trust me.")
    async def daily(self, interaction: discord.Interaction):
        if self.db.cooldown_remaining(interaction.user.id, "daily", 24*60*60) == 0:
            self.db.add_wallet(interaction.user.id, config.DAILY_AMOUNT)
            self.db.set_cooldown(interaction.user.id, "daily")
            await interaction.response.send_message(
                    f"💰 You claimed your daily ${config.DAILY_AMOUNT}!"
                )
        else:
            remaining = self.db.cooldown_remaining(interaction.user.id, "daily", 24*60*60)
            await interaction.response.send_message(
                f"⏳ You can claim your daily again in {fmt_duration(remaining)} seconds."
            )

# TODO: /work               - random WORK_MIN..WORK_MAX + random job, 1h cooldown, laptop bonus
    @app_commands.command(description="Work for money.")
    async def work(self, interaction: discord.Interaction):
        member = interaction.user
        if self.db.cooldown_remaining(member.id, "work", config.WORK_COOLDOWN) == 0:
                amount = random.randint(config.WORK_MIN, config.WORK_MAX)
                self.db.add_wallet(member.id, amount)
                self.db.set_cooldown(member.id, "work")
                await interaction.response.send_message(
                    f"💼 {member.mention} worked hard and earned ${amount}!"
                )
        else:
            remaining = self.db.cooldown_remaining(member.id, "work", config.WORK_COOLDOWN)
            await interaction.response.send_message(
                f"⏳ You can work again in {fmt_duration(remaining)} seconds."
            )

# TODO: /pay <member> <amount>
    @app_commands.command(description="Give you pal some cash")
    async def pay(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        if self.db.transfer(interaction.user.id, member.id, amount) == False:
            await interaction.response.send_message("❌ You can't afford that!")
        else:
            await interaction.response.send_message(f"💰 What a goat! {interaction.user.mention} paid {member.mention} ${amount}.")

# TODO: /deposit <amount>   - supports "all" / "half" via parse_amount
    @app_commands.command(description="Deposit money into your bank.")
    async def deposit(self, interaction: discord.Interaction, amount: str):
        available = self.db.get_balance(interaction.user.id)[0]
        parsed_amount = parse_amount(amount, available)
        if self.db.deposit(interaction.user.id, parsed_amount) == False:
            await interaction.response.send_message("❌ You can't afford that!")
        else:
            self.db.deposit(interaction.user.id, parsed_amount)
            await interaction.response.send_message(f"🏦 Deposited ${parsed_amount} into your bank.")

# TODO: /withdraw <amount>
    @app_commands.command(description="Withdraw money from your bank.")
    async def withdraw(self, interaction: discord.Interaction, amount: str):
        user_id = interaction.user.id
        cooldown_duration = 6  # 6 hours in seconds
        
        # 1. Check database/time cooldown first
        remaining = self.db.cooldown_remaining(user_id, "withdraw", cooldown_duration)
        if remaining > 0:
            await interaction.response.send_message(f"❌ You can't withdraw money for another {fmt_duration(remaining)}!", ephemeral=True)
            return

        # 2. Fetch balance and parse amount
        available = self.db.get_balance(user_id)[1]
        parsed_amount = parse_amount(amount, available)

        # 3. Perform the withdrawal once
        if not self.db.withdraw(user_id, parsed_amount):
            await interaction.response.send_message("❌ You can't afford that!", ephemeral=True)
        else:
            # 4. Set the cooldown timestamp
            self.db.set_cooldown(user_id, "withdraw")
            await interaction.response.send_message(f"🏦 Withdrew ${parsed_amount} from your bank.", ephemeral=True)

    # @app_commands.command(description="Withdraw money from your bank.")
    # async def withdraw(self, interaction: discord.Interaction, amount: str):
    #     available = self.db.get_balance(interaction.user.id)[1]
    #     parsed_amount = parse_amount(amount, available)
    #     if self.db.withdraw(interaction.user.id, parsed_amount) == False:
    #         await interaction.response.send_message("❌ You can't afford that!")
    #     elif remaining := self.db.cooldown_remaining(interaction.user.id, "withdraw", 60*60*6) > 0:
    #         await interaction.response.send_message(f"❌ You can't withdraw money for another {fmt_duration(remaining)}!")
    #     else:
    #         self.db.withdraw(interaction.user.id, parsed_amount)
    #         self.db.set_cooldown(interaction.user.id, "withdraw")
    #         await interaction.response.send_message(f"🏦 Withdrew ${parsed_amount} from your bank.")

# TODO: /leaderboard        - top 10 by net worth
    @app_commands.command(description="See the top 10 richest members.")
    async def leaderboard(self, interaction: discord.Interaction):
        leaderboard = self.db.leaderboard()
        embed = discord.Embed(title="💰 Leaderboard", color=discord.Color.gold())
        for i, (user_id, net_worth) in enumerate(leaderboard):
            user = await self.bot.fetch_user(user_id)
            embed.add_field(name=f"{i+1}. {user.name}", value=f"Net worth: ${net_worth}", inline=False)
        await interaction.response.send_message(embed=embed)

 
    # TODO: /fish               - needs a fishing_rod, uses config.FISH weights


async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))
