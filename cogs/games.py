"""Mini-games that earn coins. No betting."""

import random
from typing import Literal

import discord
from discord import app_commands
from discord.ext import commands

import config
from utils import check_cooldown, fmt


# TODO: class TriviaView(discord.ui.View) - one button per answer, only the asker can click,
#       turn the right answer green, time out after TRIVIA_TIMEOUT seconds


class Games(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

# TODO: /trivia                        - random config.TRIVIA_QUESTIONS, answer with buttons (TriviaView)
# TODO: /rps <rock|paper|scissors>     - beat the bot for RPS_REWARD


async def setup(bot: commands.Bot):
    await bot.add_cog(Games(bot))
