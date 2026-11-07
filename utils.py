"""Small formatting / parsing helpers shared by the cogs."""

import math

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
