# 🪙 Discord Economy Bot

A Discord economy bot built with Python, [discord.py](https://github.com/Rapptz/discord.py) slash commands. All the data is saved to a single JSON file, so there's no database to set up. Earn coins, bank them, gamble them, rob your friends and spend it all in the shop.

Built live in a 2 hour Discord bot workshop stream.

## Features

- 💰 **Wallet and bank:** money in your wallet can be stolen, money in the bank can't
- 📅 **Earning:** daily rewards, hourly jobs and fishing, each with its own cooldown
- 🎰 **Gambling:** coinflip and a weighted slot machine
- 🦹 **Robbing:** steal from other players' wallets, or get caught and pay up
- 🛒 **Shop and inventory:** items that actually do things (a padlock blocks robberies, a fishing rod unlocks `/fish`)
- 🏆 **Leaderboard** by net worth
- ⚙️ **Everything tunable** from one `config.py` file

## Commands

### Economy

| Command | What it does |
|---------|--------------|
| `/balance [member]` | Show wallet, bank and net worth |
| `/daily` | Claim 500 coins once every 24 hours |
| `/work` | Earn 50–200 coins once an hour |
| `/fish` | Catch something to sell (needs a 🎣 Fishing Rod, which can break) |
| `/pay <member> <amount>` | Send coins to someone |
| `/deposit <amount>` | Move coins into the bank: a number, `half` or `all` |
| `/withdraw <amount>` | Move coins back to your wallet |
| `/leaderboard` | Top 10 richest players |

### Games

| Command | What it does |
|---------|--------------|
| `/coinflip <heads/tails> <bet>` | Double or nothing |
| `/slots <bet>` | Three of a kind pays 2x to 250x, two of a kind refunds your bet |
| `/rob <member>` | 45% chance to steal 10–40% of their wallet. Fail and you pay them a fine |

### Shop

| Command | What it does |
|---------|--------------|
| `/shop` | Browse items |
| `/buy <item> [quantity]` | Buy an item |
| `/inventory [member]` | See what someone owns |

| Item | Price | Effect |
|------|-------|--------|
| 🎣 Fishing Rod | 750 | Unlocks `/fish` |
| 🔒 Padlock | 400 | Blocks one robbery, then breaks |
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

All the numbers live in [`config.py`](config.py): the currency emoji, starting balance, rewards, cooldowns, rob odds, slot machine weights and payouts, fish, and shop items. Add an item to `SHOP_ITEMS` and it appears in `/shop` and `/buy` automatically.

## Project structure

```
discord-economy-bot/
├── bot.py           # Starts the bot, loads cogs, registers slash commands
├── config.py        # All the tunable numbers
├── database.py      # Saves balances, cooldowns and items to economy.json
├── utils.py         # Formatting helpers
└── cogs/
    ├── economy.py   # balance, daily, work, fish, pay, bank, leaderboard
    ├── games.py     # coinflip, slots, rob
    ├── shop.py      # shop, buy, inventory
    └── admin.py     # addmoney, resetuser
```

## How it works

- **Cogs** keep each group of commands in its own file. `bot.py` loads them on startup.
- **All the data is one Python dict** (`{"users": {user_id: {wallet, bank, cooldowns, inventory}}}`), loaded from `economy.json` on startup and saved after every change.
- **Saves can't corrupt the file.** Each save writes to a temp file first and then swaps it in, so a crash mid-save leaves the old file intact.
- **Money can't go negative.** Every spend checks the balance first and returns `False` if you can't afford it.
- **Cooldowns are saved too**, so restarting the bot doesn't reset everyone's `/daily`.
- **Balances are global.** A player's coins follow them across every server the bot is in.

## Ideas to extend it

- Separate economies per server (key the data by server ID as well as user ID)
- Moving to SQLite once you have lots of players
- Bank interest paid out on a timer with `discord.ext.tasks`
- Blackjack with `discord.ui` buttons
- Selling items back to the shop
- Gifting items to other players
