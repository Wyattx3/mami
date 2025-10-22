# 🎮 Telegram Strategy Game

**MBTI & Zodiac Based Team Strategy Game**

A sophisticated Telegram bot game where players form teams and compete by selecting characters based on MBTI personalities and Zodiac signs.

---

## 🌟 Features

### Game Mechanics
- ✅ **9 Players, 3 Teams** - Balanced team-based gameplay
- ✅ **5 Rounds** - Strategic character selection
- ✅ **MBTI & Zodiac Scoring** - Unique compatibility system
- ✅ **Real-time Voting** - 60-second rounds with live updates
- ✅ **Team Chat** - Private communication through bot DM
- ✅ **Smart Voting Logic** - Majority, leader priority, first voter fallback
- ✅ **Character Reuse Prevention** - No duplicate selections per team

### Technical Features
- 🔐 **Dual Admin System** - Multiple admin password support
- 🗄️ **SQLite Database** - Lightweight, file-based storage
- 🤖 **AI Integration** - Gemini AI for character descriptions
- 📊 **Pre-defined Scoring** - MBTI (60%) + Zodiac (40%) compatibility
- 🎯 **One Game Per User** - Cross-channel game participation limits
- ⏱️ **Vote Time Validation** - Late vote rejection
- 🔄 **Dynamic Message Editing** - Reduced message spam

---

## 📋 Game Roles

| Round | Role | Myanmar | Description |
|-------|------|---------|-------------|
| 1 | King | ဘုရင် | Leadership qualities |
| 2 | General | စစ်သူကြီး | Bravery & courage |
| 3 | Advisor | အကြံပေး | Wisdom & intelligence |
| 4 | Farmer | လယ်သမား | Business acumen |
| 5 | Monk | ဘုန်းကြီး | Politeness & virtue |

---

## 🎯 How to Play

### 1. Start Game
```
/newgame (in group chat)
```

### 2. Join Lobby
- Click "Join" button
- Wait for 9 players total
- Game starts automatically

### 3. Team Formation
- 3 teams of 3 players each
- Random leader assignment
- Team names based on leader's username

### 4. Voting Rounds
- Each team receives 4 random characters
- Team members vote in bot's private chat
- 60 seconds per round
- Team chat available for discussion

### 5. Scoring & Winner
- MBTI compatibility: 60%
- Zodiac compatibility: 40%
- Detailed explanations provided
- Highest total score wins!

---

## 🔧 Commands

### User Commands
| Command | Description | Where |
|---------|-------------|-------|
| `/start` | Show welcome & menu | Private/Group |
| `/help` | Display help info | Anywhere |
| `/newgame` | Create new game | Group only |
| `/cancelgame` | Cancel active game | Group only |

### Admin Commands
| Command | Description | Access |
|---------|-------------|--------|
| `/addcharacter` | Add new character | Password required |

**Admin Passwords:**
- `Wyatt#9810`
- `Yuyalay2000`

---

## 📦 Installation

### Requirements
```
Python 3.13+
python-telegram-bot==22.5
google-generativeai==0.3.2
aiosqlite==0.19.0
python-dotenv==1.0.0
flask==3.0.0
```

### Local Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
TELEGRAM_BOT_TOKEN=your_bot_token
GEMINI_API_KEY=your_api_key
LOBBY_SIZE=9
TEAM_SIZE=3
ROUND_TIME=60
EOF

# Run bot
python bot.py
```

### Replit Deployment
See [REPLIT_SETUP.md](REPLIT_SETUP.md) for detailed instructions.

---

## 🗄️ Database Structure

### Tables
- **characters** - Character data (name, MBTI, zodiac, description)
- **games** - Game sessions and status
- **game_players** - Player-team assignments
- **game_rounds** - Round results and scores
- **lobby_queue** - Active lobby participants

### Minimum Data
- **12 characters** required for gameplay
- Recommended: **20-50 characters** for variety

---

## 🎨 Character System

### MBTI Types (16 types)
```
INTJ, INTP, ENTJ, ENTP
INFJ, INFP, ENFJ, ENFP
ISTJ, ISFJ, ESTJ, ESFJ
ISTP, ISFP, ESTP, ESFP
```

### Zodiac Signs (12 signs)
```
Aries, Taurus, Gemini, Cancer
Leo, Virgo, Libra, Scorpio
Sagittarius, Capricorn, Aquarius, Pisces
```

### Scoring Algorithm
- Each role has MBTI score (1-10)
- Each role has Zodiac score (1-10)
- Final = (MBTI × 0.6) + (Zodiac × 0.4)
- Rounded to 1 decimal place

---

## 🏗️ Architecture

```
tele scy/
├── bot.py                 # Main entry point
├── config.py             # Configuration
├── keep_alive.py         # Replit keep-alive
├── requirements.txt      # Dependencies
├── database/
│   └── db_manager.py    # Database operations
├── handlers/
│   ├── lobby_handler.py  # Lobby management
│   ├── game_handler.py   # Game flow control
│   └── voting_handler.py # Voting system
├── models/
│   ├── character.py      # Character model
│   ├── player.py        # Player model
│   └── game.py          # Game models
├── services/
│   ├── ai_service.py    # Gemini AI integration
│   ├── scoring_service.py # Scoring logic
│   └── team_service.py  # Team formation
└── utils/
    ├── constants.py     # Game constants
    └── helpers.py       # Helper functions
```

---

## 🔐 Security Features

- ✅ Admin password protection
- ✅ Input validation (English names only)
- ✅ SQL injection prevention
- ✅ Environment variable protection
- ✅ Permission checks for game cancellation

---

## 🐛 Troubleshooting

### Bot Not Responding
1. Check bot token in BotFather
2. Verify bot is admin in group (optional)
3. Check logs for errors

### Game Won't Start
1. Verify minimum 12 characters in database
2. Check no active game in channel
3. Ensure users not in another active game

### Voting Issues
1. Check round time hasn't expired
2. Verify bot DM is unblocked
3. Ensure character availability

### Database Errors
```bash
# Reset database
rm database/game.db
# Bot recreates on next run
```

---

## 📊 Production vs Test Mode

### Production (Default)
```
LOBBY_SIZE=9     # Full game
TEAM_SIZE=3      # 3 teams
ROUND_TIME=60    # 1 minute
```

### Test Mode
```
LOBBY_SIZE=2     # Quick test
TEAM_SIZE=2      # 1 team
ROUND_TIME=30    # 30 seconds
```

---

## 🚀 Deployment

### Supported Platforms
- ✅ **Replit** (recommended for beginners)
- ✅ **Local Server** (recommended for development)
- ✅ **VPS/Cloud** (recommended for production)
- ✅ **Heroku, Railway, Render** (with modifications)

### Replit Deployment
1. Upload files to Replit
2. Configure Secrets (environment variables)
3. Run bot
4. Setup UptimeRobot for keep-alive

See [REPLIT_SETUP.md](REPLIT_SETUP.md) for details.

---

## 📝 License

This project is for educational and entertainment purposes.

---

## 🤝 Contributing

This is a private project. Contributions are managed by the development team.

---

## 📞 Support

For issues or questions:
1. Check documentation
2. Review logs for errors
3. Verify configuration
4. Test in private chat first

---

## 🎉 Credits

**Developed for MBTI & Zodiac enthusiasts**

Combining personality psychology with strategic gameplay!

---

**Version:** 1.0.0  
**Last Updated:** October 2025  
**Status:** Production Ready ✅
