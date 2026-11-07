# 🪙 Discord Economy Bot

A Discord economy bot built with Python, [discord.py](https://github.com/Rapptz/discord.py) slash commands. All the data is saved to a single JSON file, so there's no database to set up. Earn coins from jobs, fishing and mini-games, watch your savings grow in the bank, and spend it all in the shop.

Built live in a 2 hour Discord bot workshop stream.

## Features

- 💰 **Wallet and bank:** money in the bank earns interest every day
- 📅 **Earning:** daily rewards, hourly jobs and fishing, each with its own cooldown
- 🧠 **Mini-games:** trivia with clickable buttons and rock paper scissors. You earn coins for playing; nothing is ever bet
- 🛒 **Shop and inventory:** items that actually do things (a fishing rod unlocks `/fish`, a laptop boosts `/work`)
- 🏆 **Leaderboard** by net worth
- ⚙️ **Everything tunable** from one `config.py` file

## Commands

### Economy

| Command | What it does |
|---------|--------------|
| `/balance [member]` | Show wallet, bank and net worth |
| `/daily` | Claim 500 coins once every 24 hours, plus 2% interest on your bank |
| `/work` | Earn 50–200 coins once an hour (50% more with a 💻 Laptop) |
| `/fish` | Catch something to sell (needs a 🎣 Fishing Rod, which can break) |
| `/pay <member> <amount>` | Send coins to someone |
| `/deposit <amount>` | Move coins into the bank to earn interest: a number, `half` or `all` |
| `/withdraw <amount>` | Move coins back to your wallet |
| `/leaderboard` | Top 10 richest players |

### Games

| Command | What it does |
|---------|--------------|
| `/trivia` | Answer a multiple-choice question with buttons to win 100 coins |
| `/rps <rock/paper/scissors>` | Beat the bot at rock paper scissors to win 30 coins |

### Shop

| Command | What it does |
|---------|--------------|
| `/shop` | Browse items |
| `/buy <item> [quantity]` | Buy an item |
| `/inventory [member]` | See what someone owns |

| Item | Price | Effect |
|------|-------|--------|
| 🎣 Fishing Rod | 750 | Unlocks `/fish` |
| 💻 Laptop | 1,500 | `/work` pays 50% more |
| 🏆 Golden Trophy | 100,000 | Does nothing. Proves everything. |

### Admin

These are hidden from anyone without Administrator permission.

| Command | What it does |
|---------|--------------|
| `/addmoney <member> <amount>` | Give someone coins |
| `/resetuser <member>` | Wipe someone's coins, items and cooldowns |

## Getting started

You'll need **Python 3.10 or newer**.

### 1. Create the bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and click **New Application**.
2. Open the **Bot** tab and click **Reset Token**. Copy the token and keep it secret.
3. Copy your **Application ID** from the **General Information** tab.
4. Invite the bot to your server with this link, swapping in your Application ID:

   ```
   https://discord.com/oauth2/authorize?client_id=YOUR_APPLICATION_ID&scope=bot+applications.commands&permissions=18432
   ```

   This gives it the **Send Messages** and **Embed Links** permissions, which is all it needs.

### 2. Install

```bash
git clone https://github.com/TalenMud/discord-economy-bot.git
cd discord-economy-bot
python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

Then install the requirements:

```bash
pip install -r requirements.txt
```

### 3. Configure

Copy `.env.example` to `.env` and fill it in:

```env
DISCORD_TOKEN=your-bot-token
GUILD_ID=
```

| Key | Required | What it's for |
|-----|----------|---------------|
| `DISCORD_TOKEN` | Yes | Your bot's token from step 1 |
| `GUILD_ID` | No | A server ID to register commands in **only that server**, where they show up instantly. Handy while developing. Leave it blank so the bot works in every server it joins. |

### 4. Run

```bash
python bot.py
```

Player data is saved to `economy.json`, which is created automatically the first time someone uses a command. Open it any time to see exactly what's stored.

## Customizing

All the numbers live in [`config.py`](config.py): the currency emoji, starting balance, rewards, cooldowns, bank interest, fish, trivia questions and shop items. Add an item to `SHOP_ITEMS` and it appears in `/shop` and `/buy` automatically. Add a question to `TRIVIA_QUESTIONS` and it's in the game.

## Project structure

```
discord-economy-bot/
├── bot.py           # Starts the bot, loads cogs, registers slash commands
├── config.py        # All the tunable numbers
├── database.py      # Saves balances, cooldowns and items to economy.json
├── utils.py         # Formatting and cooldown helpers
└── cogs/
    ├── economy.py   # balance, daily, work, fish, pay, bank, leaderboard
    ├── games.py     # trivia (buttons), rock paper scissors
    ├── shop.py      # shop, buy, inventory
    └── admin.py     # addmoney, resetuser
```

## How it works

- **Cogs** keep each group of commands in its own file. `bot.py` loads them on startup.
- **All the data is one Python dict** (`{"users": {user_id: {wallet, bank, cooldowns, inventory}}}`), loaded from `economy.json` on startup and saved after every change.
- **Saves can't corrupt the file.** Each save writes to a temp file first and then swaps it in, so a crash mid-save leaves the old file intact.
- **Money can't go negative.** Every spend checks the balance first and returns `False` if you can't afford it.
- **Cooldowns are saved too**, so restarting the bot doesn't reset everyone's `/daily`.
- **Trivia uses `discord.ui.View`**, Discord's buttons. Only the person who asked can answer, and the buttons lock after one click or 20 seconds.
- **Balances are global.** A player's coins follow them across every server the bot is in.

## Ideas to extend it

- Separate economies per server (key the data by server ID as well as user ID)
- Moving to SQLite once you have lots of players
- More trivia categories, or questions from an online trivia API
- A `/quest` system with daily goals
- Selling items back to the shop
- Gifting items to other players

## License

[MIT](LICENSE)
