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

# TODO: add "cogs.games" as we build it
COGS = ["cogs.economy", "cogs.shop", "cogs.admin"]

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
            log.info(
                "Synced %d commands to guild %s: %s",
                len(synced), GUILD_ID, ", ".join(c.name for c in synced),
            )
        else:
            synced = await self.tree.sync()
            log.info(
                "Synced %d global commands: %s",
                len(synced), ", ".join(c.name for c in synced),
            )
            log.warning(
                "GUILD_ID is not set, so Discord may take up to an hour to show new "
                "commands. Set GUILD_ID in .env to sync instantly while developing."
            )

    async def on_ready(self) -> None:
        log.info("Logged in as %s (%s)", self.user, self.user.id)


bot = EconomyBot()

# TODO: global error handler (@bot.tree.error) for cooldowns / missing permissions


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("DISCORD_TOKEN is missing. Copy .env.example to .env and fill it in.")
    bot.run(TOKEN)
