"""Admin-only commands."""

import discord
from discord import app_commands
from discord.ext import commands

from utils import fmt


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    # TODO: /addmoney <member> <amount>   - @app_commands.default_permissions(administrator=True)
    # TODO: /resetuser <member>


async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
