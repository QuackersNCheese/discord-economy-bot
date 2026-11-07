"""Core money commands."""

import random

import discord
from discord import app_commands
from discord.ext import commands

import config
from utils import check_cooldown, fmt, parse_amount


class Economy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    @app_commands.command(description="Check the bot is alive.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"🏓 Pong! {round(self.bot.latency * 1000)}ms")

    # TODO: /balance [member]   - embed with wallet, bank, net worth
    # TODO: /daily              - DAILY_AMOUNT, 24h cooldown, plus bank interest (BANK_INTEREST_RATE)
    # TODO: /work               - random WORK_MIN..WORK_MAX + random job, 1h cooldown, laptop bonus
    # TODO: /pay <member> <amount>
    # TODO: /deposit <amount>   - supports "all" / "half" via parse_amount
    # TODO: /withdraw <amount>
    # TODO: /leaderboard        - top 10 by net worth
    # TODO: /fish               - needs a fishing_rod, uses config.FISH weights


async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))
