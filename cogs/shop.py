"""The shop."""

import discord
from discord import app_commands
from discord.ext import commands

import config
from utils import fmt


class Shop(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    # TODO: /shop                     - embed listing config.SHOP_ITEMS
    # TODO: /buy <item> [quantity]    - item as app_commands.choices
    # TODO: /inventory [member]


async def setup(bot: commands.Bot):
    await bot.add_cog(Shop(bot))
