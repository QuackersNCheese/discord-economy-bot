"""All the tunable numbers for the economy live here."""

CURRENCY = "🪙"
STARTING_BALANCE = 100

# Earning
DAILY_AMOUNT = 100
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
    ("🐢 Turtle", 250, 8),
    ("🦆 Duck", 120, 10),
    ("🐲 Iguana", 100, 10),
    ("🐸 Frog", 60, 18),
    ("🦐 Freshwater Shrimp", 80, 15),
    ("🦞 Crayfish", 120, 12),
    ("🐍 Water Snake", 200, 8),
    ("🦫 Beaver", 350, 5),
    ("🦦 Otter", 450, 4),
    ("🦢 Swan", 550, 3),
    ("🐊 Alligator", 1_200, 1),
    ("🪱 Leech", 0, 8),
    ("🎏 Koi", 400, 4),
    ("🐿️ Squirrel", 90, 10),
    ("🦎 Lizard", 70, 14),
    ("🦀 Crab", 50, 20),
    ("🪼 Jellyfish", 30, 22),
    ("🐙 Octopus", 300, 6),
    ("🦩 Flamingo", 500, 3),
    ("🦭 Seal", 800, 2),
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
        "description": "All command earnings pay 50% more. Only one counts.",
        "earn_bonus": 0.5,
        "unique": True,
    },
    "ruby_charm": {
        "name": "Ruby Charm",
        "emoji": "❤️",
        "price": 2_500,
        "description": "Command earnings pay 10% more. Stacks with other charms.",
        "earn_bonus": 0.10,
        "unique": True,
    },
    "sapphire_charm": {
        "name": "Sapphire Charm",
        "emoji": "💙",
        "price": 5_000,
        "description": "Command earnings pay 20% more. Stacks with other charms.",
        "earn_bonus": 0.20,
        "unique": True,
    },
    "emerald_charm": {
        "name": "Emerald Charm",
        "emoji": "💚",
        "price": 10_000,
        "description": "Command earnings pay 30% more. Stacks with other charms.",
        "earn_bonus": 0.30,
        "unique": True,
    },
    "amethyst_charm": {
        "name": "Amethyst Charm",
        "emoji": "💜",
        "price": 20_000,
        "description": "Command earnings pay 40% more. Stacks with other charms.",
        "earn_bonus": 0.40,
        "unique": True,
    },
    "diamond_charm": {
        "name": "Diamond Charm",
        "emoji": "💎",
        "price": 50_000,
        "description": "Command earnings pay 60% more. Stacks with other charms.",
        "earn_bonus": 0.60,
        "unique": True,
    },
    "trophy": {
        "name": "Golden Trophy",
        "emoji": "🏆",
        "price": 100_000,
        "description": "Does nothing. Proves everything.",
    },
}
