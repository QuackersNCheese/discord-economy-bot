"""Ways to win (and lose) money."""

import random
from typing import Literal

import discord
from discord import app_commands
from discord.ext import commands

import config
from utils import fmt, fmt_duration


class Games(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    # TODO: /coinflip <heads|tails> <bet>  - double or nothing
    # TODO: /slots <bet>                   - 3 reels using config.SLOT_SYMBOLS
    # TODO: /rob <member>                  - padlock check, success chance, fine on failure


async def setup(bot: commands.Bot):
    await bot.add_cog(Games(bot))
