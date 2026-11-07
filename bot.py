"""Entry point: python bot.py"""

import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from database import Database

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")  # optional: syncs commands instantly to one server

# TODO: add "cogs.games", "cogs.shop", "cogs.admin" as we build them
COGS = ["cogs.economy"]

log = logging.getLogger("economy")


class EconomyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix=commands.when_mentioned, intents=intents)
        self.db = Database("economy.json")

    async def setup_hook(self) -> None:
        self.db.load()
        for cog in COGS:
            await self.load_extension(cog)

        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
        else:
            synced = await self.tree.sync()
        log.info("Synced %d commands", len(synced))

    async def on_ready(self) -> None:
        log.info("Logged in as %s (%s)", self.user, self.user.id)


bot = EconomyBot()

# TODO: global error handler (@bot.tree.error) for cooldowns / missing permissions


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("DISCORD_TOKEN is missing. Copy .env.example to .env and fill it in.")
    bot.run(TOKEN)
