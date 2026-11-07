"""All the tunable numbers for the economy live here."""

CURRENCY = "🪙"
STARTING_BALANCE = 100

# Earning
DAILY_AMOUNT = 500
DAILY_COOLDOWN = 24 * 60 * 60  # seconds

WORK_MIN = 50
WORK_MAX = 200
WORK_COOLDOWN = 60 * 60

JOBS = [
    "flipped burgers",
    "walked some dogs",
    "fixed a printer (somehow)",
    "streamed for 6 hours",
    "debugged someone's Python",
    "delivered pizzas",
    "mowed a lawn",
    "moderated a Discord server",
]

# Fishing (needs a fishing rod from the shop)
FISH_COOLDOWN = 5 * 60
ROD_BREAK_CHANCE = 0.05
# (name, value, weight) - higher weight = more common
FISH = [
    ("🥾 Old Boot", 0, 15),
    ("🐟 Cod", 40, 40),
    ("🐠 Tropical Fish", 90, 25),
    ("🐡 Pufferfish", 150, 12),
    ("🦈 Shark", 600, 5),
    ("💎 Sunken Treasure", 2000, 1),
]

# Robbing
ROB_COOLDOWN = 30 * 60
ROB_SUCCESS_CHANCE = 0.45
ROB_MIN_VICTIM_WALLET = 100
ROB_STEAL_MIN = 0.10  # fraction of victim's wallet
ROB_STEAL_MAX = 0.40
ROB_FINE_MIN = 50
ROB_FINE_MAX = 250

# Slots: (symbol, weight, payout multiplier for three of a kind)
# Two of a kind refunds the bet. House edge works out to roughly 6%.
SLOT_SYMBOLS = [
    ("🍒", 40, 2),
    ("🍋", 30, 4),
    ("🍇", 20, 10),
    ("💎", 8, 50),
    ("7️⃣", 2, 250),
]

# Shop
SHOP_ITEMS = {
    "fishing_rod": {
        "name": "Fishing Rod",
        "emoji": "🎣",
        "price": 750,
        "description": "Lets you use /fish. Might break.",
    },
    "padlock": {
        "name": "Padlock",
        "emoji": "🔒",
        "price": 400,
        "description": "Blocks one robbery attempt, then breaks.",
    },
    "trophy": {
        "name": "Golden Trophy",
        "emoji": "🏆",
        "price": 100_000,
        "description": "Does nothing. Proves everything.",
    },
}
