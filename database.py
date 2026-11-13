"""Stores everything in one Python dict, saved to a JSON file.

The file looks like this:

{
  "users": {
    "123456789": {
      "wallet": 100,
      "bank": 0,
      "cooldowns": {"daily": 1730000000.0},
      "inventory": {"laptop": 1}
    }
  }
}

JSON keys are always strings, so user IDs are stored as str(user_id).
"""

import json
import os
import time

from config import SHOP_ITEMS, STARTING_BALANCE


class Database:
    def __init__(self, path: str):
        self.path = path
        self.data = {"users": {}}

    def load(self) -> None:
        if os.path.exists(self.path):
            with open(self.path, encoding="utf-8") as f:
                self.data = json.load(f)

    def save(self) -> None:
        # Write to a temp file, then swap it in, so a crash mid-save can't corrupt the real file.
        temp_path = self.path + ".tmp"
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)
        os.replace(temp_path, self.path)

    def _user(self, user_id: int) -> dict:
        """Get a user's record, creating it with STARTING_BALANCE if needed.
        Keys: wallet, bank, cooldowns (dict), inventory (dict)."""
        user_id_str = str(user_id)
        if user_id_str not in self.data['users']:
            self.data['users'][user_id_str] = {
                "wallet": STARTING_BALANCE,
                "bank": 0,
                "cooldowns": {},
                "inventory": {},
            }
        return self.data['users'][user_id_str]

    # ---------- money ----------

    def get_balance(self, user_id: int) -> tuple[int, int]:
        """Return (wallet, bank)."""
        return self._user(user_id)["wallet"], self._user(user_id)["bank"]

    def add_wallet(self, user_id: int, amount: int) -> None:
        self._user(user_id)["wallet"] += amount
        self._user(user_id)["wallet"] = max(0, self._user(user_id)["wallet"])  # no negative balances
        self.save()

    def add_bank(self, user_id: int, amount: int) -> None:
        # TODO
        ...

    def remove_wallet(self, user_id: int, amount: int) -> bool:
        """Take money from a wallet. Return False (change nothing) if they can't afford it."""
        self._user(user_id)["wallet"] -= amount
        if self._user(user_id)["wallet"] < 0:
            self._user(user_id)["wallet"] += amount  # revert
            self.save()
            return False
        self.save()
        return True

    def transfer(self, sender_id: int, receiver_id: int, amount: int) -> bool:
        """Move money between wallets. Return False if the sender can't afford it."""
        if self.remove_wallet(sender_id, amount) == False:
            return False
        self._user(receiver_id)["wallet"] += amount
        self.save()
        return True

    def deposit(self, user_id: int, amount: int) -> bool:
        if self._user(user_id)["wallet"] < amount:
                return False
            
        self._user(user_id)["wallet"] -= amount
        self._user(user_id)["bank"] += amount
        self.save()
        return True

    def withdraw(self, user_id: int, amount: int) -> bool:
        if self._user(user_id)["bank"] < amount:
            return False
        self._user(user_id)["bank"] -= amount
        self._user(user_id)["wallet"] += amount
        self.save()
        return True

    def leaderboard(self, limit: int = 10) -> list[tuple[int, int]]:
        """Return [(user_id, net_worth), ...] richest first."""
        users = self.data["users"]
        leaderboard = []
        for user_id_str, record in users.items():
            net_worth = record["wallet"] + record["bank"]
            leaderboard.append((int(user_id_str), net_worth))
        leaderboard.sort(key=lambda x: x[1], reverse=True)
        return leaderboard[:limit]

    # ---------- cooldowns ----------

    def cooldown_remaining(self, user_id: int, name: str, seconds: int) -> float:
        """Seconds left before `name` can be used again (0 if ready). Hint: time.time()"""
        user = self._user(user_id)
        last_used = user["cooldowns"].get(name, 0)
        now = time.time()
        remaining = (last_used + seconds) - now
        return max(0, remaining)

    def set_cooldown(self, user_id: int, name: str) -> None:
        user = self._user(user_id)
        user["cooldowns"][name] = time.time()
        self.save()

    # ---------- inventory ----------

    def add_item(self, user_id: int, item_id: str, quantity: int = 1) -> None:
        user = self._user(user_id)
        user["inventory"][item_id] = user["inventory"].get(item_id, 0) + quantity
        self.save()

    def buy_item(self, user_id: int, item_id: str, quantity: int = 1) -> bool:
        """Buy an item from the shop. Return False if invalid or unaffordable."""
        if quantity < 1:
            return False
        item = SHOP_ITEMS.get(item_id)
        if item is None:
            return False
        if not self.remove_wallet(user_id, item["price"] * quantity):
            return False
        self.add_item(user_id, item_id, quantity)
        return True

    def remove_item(self, user_id: int, item_id: str, quantity: int = 1) -> bool:
        """Take items out of an inventory. Return False if they don't have enough."""
        user = self._user(user_id)
        count = user["inventory"].get(item_id, 0)
        if count < quantity:
            return False
        if count == quantity:
            del user["inventory"][item_id]
        else:
            user["inventory"][item_id] = count - quantity
        self.save()
        return True

    def get_item_count(self, user_id: int, item_id: str) -> int:
        return self._user(user_id)["inventory"].get(item_id, 0)

    def get_inventory(self, user_id: int) -> list[tuple[str, int]]:
        """Return [(item_id, count), ...] in the order items were obtained."""
        return list(self._user(user_id)["inventory"].items())

    def reset_user(self, user_id: int) -> None:
        """Wipe someone's dollars, items and cooldowns, back to a fresh account."""
        self.data["users"].pop(str(user_id), None)
        self._user(user_id)
        self.save()
