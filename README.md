# Telegram MBTI Strategy Game

MBTI နှင့် Zodiac signs ကို အခြေခံထားတဲ့ team-based strategy game for Telegram

## Features

- 🎮 9 players, 3 teams (3 players per team)
- 🎯 5 rounds of character voting
- 🤖 AI-powered character-role matching (Gemini)
- 🏆 Real-time scoring and results
- 📊 MBTI and Zodiac-based personality system

## Requirements

- Python 3.8+
- Telegram Bot Token
- Google Gemini API Key
- VPS or local server

## Installation

### 1. Clone the repository

```bash
cd /path/to/your/directory
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here
LOBBY_SIZE=9
TEAM_SIZE=3
ROUND_TIME=60
```

### 5. Initialize database

The database will be automatically created when you first run the bot.

### 6. Add characters

Before playing, you need to add at least 12 characters to the database:

```bash
python bot.py
# Then use /addcharacter command in Telegram
```

**Character Addition Process:**
1. Use `/addcharacter` command
2. Enter character name (English letters only)
3. Select MBTI type from buttons
4. Select Zodiac sign from buttons
5. AI automatically generates description
6. Enter admin password: `Wyatt#9810`
7. Character is saved to database

## Getting API Keys

### Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the instructions
4. Copy the bot token

### Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the API key

## Usage

### Start the bot

```bash
python bot.py
```

### Bot Commands

- `/start` - Welcome message and info
- `/help` - Game rules and instructions
- `/newgame` - Create a new game lobby
- `/addcharacter` - Add a new character (Admin only, requires password)
- `/stats` - View statistics
- `/cancel` - Cancel current operation

### Game Flow

1. **Create Lobby**: Use `/newgame` to create a lobby
2. **Join**: Players click "Join Game" button
3. **Auto-start**: Game starts automatically when 9 players join
4. **Team Formation**: Players are randomly divided into 3 teams
5. **5 Rounds of Voting**:
   - Round 1: ဘုရင် (King/Leader)
   - Round 2: စစ်သူကြီး (Warrior)
   - Round 3: အကြံပေး (Advisor)
   - Round 4: လယ်သမား (Farmer)
   - Round 5: ဘုန်းကြီး (Monk)
6. **Voting**: Each team votes for characters (60 seconds per round)
7. **Scoring**: AI scores character-role compatibility
8. **Results**: Team with highest score wins!

## Project Structure

```
tele scy/
├── bot.py                    # Main bot entry point
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
├── .env                      # Environment variables (not in git)
├── database/
│   ├── db_manager.py        # Database operations
│   └── game.db              # SQLite database (auto-created)
├── models/
│   ├── character.py         # Character model
│   ├── game.py              # Game state model
│   └── player.py            # Player model
├── handlers/
│   ├── lobby_handler.py     # Lobby management
│   ├── game_handler.py      # Game flow
│   └── voting_handler.py    # Voting system
├── services/
│   ├── ai_service.py        # Gemini AI integration
│   ├── team_service.py      # Team management
│   └── scoring_service.py   # Scoring logic
└── utils/
    ├── constants.py         # Game constants
    └── helpers.py           # Helper functions
```

## Deployment

### VPS Deployment

1. **Upload files to VPS**:

```bash
scp -r "tele scy/" user@your-vps-ip:/path/to/deployment/
```

2. **SSH into VPS**:

```bash
ssh user@your-vps-ip
```

3. **Navigate to directory**:

```bash
cd /path/to/deployment/tele\ scy/
```

4. **Setup virtual environment**:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. **Configure .env file**:

```bash
nano .env
# Add your API keys
```

6. **Run with screen/tmux**:

```bash
screen -S telegram-bot
python bot.py
# Press Ctrl+A then D to detach
```

Or use systemd service:

```bash
sudo nano /etc/systemd/system/telegram-game.service
```

```ini
[Unit]
Description=Telegram Strategy Game Bot
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/tele scy
Environment="PATH=/path/to/tele scy/venv/bin"
ExecStart=/path/to/tele scy/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-game
sudo systemctl start telegram-game
```

## Game Logic

### Voting System

- Each team sees 4 random characters
- Team members vote within 60 seconds
- Vote resolution:
  - 2+ votes for same character → Selected
  - All different votes → First voter's choice wins
  - No votes → "Optional" (no character selected)

### Scoring System

- AI evaluates character-role compatibility
- Score range: 1-10 per role
- Based on MBTI and Zodiac traits
- Team with highest total score wins

### Character-Role Matching

Each role has suitable MBTI types:
- **ဘုရင်** (Leader): ENTJ, ENFJ, ESTJ, ENTP
- **စစ်သူကြီး** (Warrior): ESTP, ISTP, ESTJ, ISTJ
- **အကြံပေး** (Advisor): INTJ, INTP, INFJ, ENTP
- **လယ်သမား** (Farmer): ISTJ, ISFJ, ESTJ, ESFJ
- **ဘုန်းကြီး** (Monk): INFJ, INFP, ENFJ, ISFJ

## Troubleshooting

### Bot doesn't respond

- Check if bot token is correct
- Verify bot is running: `ps aux | grep bot.py`
- Check logs for errors

### Not enough characters error

- Add more characters using `/addcharacter`
- Minimum required: 12 characters

### AI scoring fails

- Verify Gemini API key is valid
- Check API quota limits
- Bot will use fallback scoring if AI fails

### Database errors

- Delete `database/game.db` and restart bot
- Database will be recreated automatically

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is for educational purposes.

## Support

For questions or issues, contact the developer.

---

Made with ❤️ in Myanmar 🇲🇲


