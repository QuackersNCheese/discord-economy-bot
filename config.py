"""All the tunable numbers for the economy live here."""

CURRENCY = "🪙"
STARTING_BALANCE = 100

# Earning
DAILY_AMOUNT = 500
DAILY_COOLDOWN = 24 * 60 * 60  # seconds

WORK_MIN = 50
WORK_MAX = 200
WORK_COOLDOWN = 60 * 60
LAPTOP_BONUS = 1.5  # /work multiplier if you own a laptop

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

# Bank: interest is paid into your bank each time you claim /daily
BANK_INTEREST_RATE = 0.02  # 2%
BANK_INTEREST_CAP = 1_000

# Trivia: answer with buttons, no betting
TRIVIA_REWARD = 100
TRIVIA_COOLDOWN = 2 * 60
TRIVIA_TIMEOUT = 20  # seconds to answer
# (question, correct answer, [wrong answers])
TRIVIA_QUESTIONS = [
    ("What does CPU stand for?", "Central Processing Unit",
     ["Computer Personal Unit", "Central Program Utility", "Core Processing Utility"]),
    ("Which planet is known as the Red Planet?", "Mars", ["Venus", "Jupiter", "Mercury"]),
    ("What language is this bot written in?", "Python", ["JavaScript", "Java", "C++"]),
    ("How many sides does a hexagon have?", "6", ["5", "7", "8"]),
    ("What is the largest ocean on Earth?", "Pacific", ["Atlantic", "Indian", "Arctic"]),
    ("What does HTML stand for?", "HyperText Markup Language",
     ["HighText Machine Language", "HyperTool Markup Language", "Hyperlink Text Management Language"]),
    ("What is 7 x 8?", "56", ["54", "63", "48"]),
    ("Which animal is the fastest on land?", "Cheetah", ["Lion", "Horse", "Greyhound"]),
    ("What number is 101 in binary?", "5", ["3", "6", "10"]),
    ("Which gas do plants take in from the air?", "Carbon dioxide", ["Oxygen", "Nitrogen", "Helium"]),
    ("What year did Discord launch?", "2015", ["2013", "2017", "2019"]),
    ("What does MLH stand for?", "Major League Hacking",
     ["Mega Linux Hub", "Main Line Hackers", "Modern Language Hub"]),
]

# Rock paper scissors against the bot, no betting
RPS_REWARD = 30
RPS_COOLDOWN = 30

# Shop
SHOP_ITEMS = {
    "fishing_rod": {
        "name": "Fishing Rod",
        "emoji": "🎣",
        "price": 750,
        "description": "Lets you use /fish. Might break.",
    },
    "laptop": {
        "name": "Laptop",
        "emoji": "💻",
        "price": 1_500,
        "description": "/work pays 50% more. Stacks? No. Worth it? Yes.",
    },
    "trophy": {
        "name": "Golden Trophy",
        "emoji": "🏆",
        "price": 100_000,
        "description": "Does nothing. Proves everything.",
    },
}
