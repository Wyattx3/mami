# 🚀 Replit Deployment Guide

## Telegram Strategy Game - MBTI & Zodiac Based

---

## 📋 Prerequisites

1. **Telegram Bot Token**
   - Get from [@BotFather](https://t.me/BotFather)
   - Command: `/newbot`

2. **Gemini API Key**
   - Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Free tier available

---

## 🔧 Setup Steps

### 1. Create New Repl

1. Go to [Replit](https://replit.com)
2. Click "Create Repl"
3. Choose "Import from GitHub" or "Upload files"
4. Select Python as language

### 2. Upload Files

Upload all files from your project:
```
bot.py
config.py
keep_alive.py
requirements.txt
.replit
database/
  └── db_manager.py
handlers/
  ├── game_handler.py
  ├── lobby_handler.py
  └── voting_handler.py
models/
  ├── character.py
  ├── game.py
  └── player.py
services/
  ├── ai_service.py
  ├── scoring_service.py
  └── team_service.py
utils/
  ├── constants.py
  └── helpers.py
```

### 3. Configure Environment Variables

Click on "Secrets" (🔒 icon) and add:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here
LOBBY_SIZE=9
TEAM_SIZE=3
ROUND_TIME=60
REPLIT_DEPLOYMENT=true
```

**Important:** 
- Replace `your_bot_token_here` with actual bot token
- Replace `your_gemini_api_key_here` with actual API key
- Set `REPLIT_DEPLOYMENT=true` to enable keep-alive

### 4. Install Dependencies

Replit will auto-install from `requirements.txt`:
- python-telegram-bot==22.5
- google-generativeai==0.3.2
- aiosqlite==0.19.0
- python-dotenv==1.0.0
- flask==3.0.0

### 5. Run the Bot

Click the "Run" button or use:
```bash
python bot.py
```

---

## 🎮 Game Configuration

### Production Mode (Default)
```
LOBBY_SIZE=9    # 9 players
TEAM_SIZE=3     # 3 teams of 3
ROUND_TIME=60   # 60 seconds per round
```

### Test Mode
```
LOBBY_SIZE=2    # 2 players
TEAM_SIZE=2     # 1 team of 2
ROUND_TIME=30   # 30 seconds per round
```

---

## 🔐 Admin Passwords

Two admin passwords are configured:
1. `Wyatt#9810`
2. `Yuyalay2000`

Use these to add characters via `/addcharacter` command.

---

## 📊 Database

SQLite database will be automatically created at:
```
database/game.db
```

**Initial Setup:**
- Database initializes on first run
- Add characters using `/addcharacter` command
- Minimum 12 characters required

---

## 🌐 Keep Alive (Free Tier)

For Replit free tier, the bot includes a keep-alive server:
- Runs on port 8080
- Health check: `https://your-repl.repl.co/health`
- Use [UptimeRobot](https://uptimerobot.com) to ping every 5 minutes

**Setup UptimeRobot:**
1. Create account at uptimerobot.com
2. Add new monitor
3. Type: HTTP(s)
4. URL: `https://your-repl-name.your-username.repl.co/`
5. Interval: 5 minutes

---

## 🎯 Bot Commands

### User Commands
- `/start` - Welcome message & menu
- `/help` - Show help information
- `/newgame` - Start new game (group only)
- `/cancelgame` - Cancel active game (admin/player)

### Admin Commands
- `/addcharacter` - Add new character (requires password)

---

## 🏗️ Game Structure

### Teams & Players
- **9 Players** join lobby
- **3 Teams** (3 players each)
- Random team leader assignment
- Team names based on leader username

### Rounds & Roles
- **5 Rounds** total
- **4 Characters** shown per round
- **60 Seconds** voting time

**Roles:**
1. ဘုရင် (King) - Leader
2. စစ်သူကြီး (General) - Brave
3. အကြံပေး (Advisor) - Wise
4. လယ်သမား (Farmer) - Business
5. ဘုန်းကြီး (Monk) - Polite

### Scoring
- MBTI compatibility: 60%
- Zodiac compatibility: 40%
- Score range: 1-10 per role
- Highest total score wins

---

## 🐛 Troubleshooting

### Bot Not Responding
1. Check Secrets are set correctly
2. Verify bot token with BotFather
3. Check Repl is running (not sleeping)

### Database Errors
```bash
# Reset database
rm database/game.db
# Bot will recreate on next run
```

### Keep Alive Issues
1. Verify `REPLIT_DEPLOYMENT=true` in Secrets
2. Check Flask is installed
3. Visit `https://your-repl.repl.co/` to test

### Gemini API Errors
- Verify API key is correct
- Check quota limits (free tier)
- Bot uses fallback descriptions if API fails

---

## 📱 Adding to Telegram Group

1. Get bot username from BotFather
2. Add bot to your group
3. Make bot admin (optional, for better UX)
4. Use `/start` in group to see menu
5. Click "New Game" or use `/newgame`

---

## 🔄 Updates & Maintenance

### Update Bot Code
1. Edit files in Repl
2. Click "Run" to restart
3. Changes apply immediately

### Add Characters
1. Use `/addcharacter` in private chat with bot
2. Enter admin password when prompted
3. Minimum 12 characters required for game

### Database Backup
Download `database/game.db` from Repl files regularly

---

## 💡 Tips

1. **Performance:** Free tier may sleep after inactivity
2. **Always On:** Use UptimeRobot to keep bot awake
3. **Characters:** Add 20-50 for best variety
4. **Testing:** Use test mode (LOBBY_SIZE=2) first
5. **Monitoring:** Check Repl logs for errors

---

## 📞 Support

If you encounter issues:
1. Check Repl console logs
2. Verify all Secrets are set
3. Test bot commands in private chat first
4. Check Telegram Bot API status

---

## 🎉 You're Ready!

Your Telegram Strategy Game bot is now deployed on Replit!

**Next Steps:**
1. Add characters using `/addcharacter`
2. Invite friends to Telegram group
3. Start game with `/newgame`
4. Enjoy! 🎮

---

**Made with ❤️ for MBTI & Zodiac enthusiasts**

