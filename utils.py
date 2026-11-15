"""Small formatting / parsing helpers shared by the cogs."""

import math

import discord

from config import CURRENCY


def fmt(amount: int) -> str:
    """Format an amount of money, e.g. 🪙 **1,250**."""
    return f"{CURRENCY} **{amount:,}**"


def fmt_duration(seconds: float) -> str:
    """Turn a number of seconds into something like '1h 5m' or '42s'."""
    seconds = max(1, math.ceil(seconds))
    hours, rem = divmod(seconds, 3600)
    minutes, secs = divmod(rem, 60)
    parts = []
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if secs and not hours:
        parts.append(f"{secs}s")
    return " ".join(parts)


def parse_amount(text: str, available: int) -> int | None:
    """Parse '500', '1,000', 'all', 'max' or 'half'. Returns None if invalid."""
    text = text.strip().lower().replace(",", "")
    if text in ("all", "max"):
        return available
    if text == "half":
        return available // 2
    if text.isdigit():
        return int(text)
    return None


def apply_earn_bonus(db, user_id: int, amount: int) -> tuple[int, str]:
    """Apply owned item bonuses to a command reward."""
    items = db.get_earn_bonus_items(user_id)
    if not items or amount <= 0:
        return amount, ""
    total = sum(item["earn_bonus"] for item in items)
    boosted = round(amount * (1 + total))
    parts = ", ".join(
        f"{item['emoji']} +{round(item['earn_bonus'] * 100)}%" for item in items
    )
    return boosted, f"\n✨ Earnings bonus: {parts} (+{round(total * 100)}%)"


async def check_cooldown(db, interaction: discord.Interaction, name: str, seconds: int) -> bool:
    """If the user is on cooldown for /name, tell them and return True."""
    remaining = db.cooldown_remaining(interaction.user.id, name, seconds)
    if remaining > 0:
        await interaction.response.send_message(
            f"⏳ You can use `/{name}` again in **{fmt_duration(remaining)}**.",
            ephemeral=True,
        )
        return True
    return False
