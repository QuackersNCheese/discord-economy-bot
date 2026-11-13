"""The shop."""

import discord
from discord import app_commands
from discord.ext import commands

import config
from utils import fmt


SHOP_CHOICES = [
    app_commands.Choice(name=f"{item['emoji']} {item['name']}", value=item_id)
    for item_id, item in config.SHOP_ITEMS.items()
]


class Shop(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.db

    @app_commands.command(description="Browse items in the shop.")
    async def shop(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🛒 Shop",
            description="Buy something with `/buy <item> [quantity]`.",
            color=discord.Color.gold(),
        )
        for item in config.SHOP_ITEMS.values():
            embed.add_field(
                name=f"{item['emoji']} {item['name']} — {fmt(item['price'])}",
                value=item["description"],
                inline=False,
            )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="See what you or someone else owns.")
    async def inventory(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        items = self.db.get_inventory(member.id)
        if not items:
            await interaction.response.send_message(f"📦 {member.mention} doesn't own anything yet.")
            return
        lines = []
        for item_id, count in items:
            item = config.SHOP_ITEMS.get(item_id, {"name": item_id, "emoji": "📦"})
            lines.append(f"{item['emoji']} **{item['name']}** x{count}")
        await interaction.response.send_message(
            f"📦 {member.mention} owns:\n" + "\n".join(lines)
        )

    @app_commands.command(description="Buy an item from the shop.")
    @app_commands.describe(item="The item to buy.", quantity="How many to buy.")
    @app_commands.choices(item=SHOP_CHOICES)
    async def buy(
        self,
        interaction: discord.Interaction,
        item: app_commands.Choice[str],
        quantity: int = 1,
    ):
        if quantity < 1:
            await interaction.response.send_message(
                "❌ Quantity must be at least 1.", ephemeral=True
            )
            return

        shop_item = config.SHOP_ITEMS[item.value]
        total = shop_item["price"] * quantity

        if not self.db.buy_item(interaction.user.id, item.value, quantity):
            await interaction.response.send_message(
                "❌ You can't afford that!", ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"{shop_item['emoji']} Bought **{quantity}x {shop_item['name']}** for {fmt(total)}!"
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Shop(bot))
