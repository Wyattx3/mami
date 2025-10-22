# ⚡ Quick Start Guide - Replit Deployment

## 🚀 5-Minute Setup

### 1️⃣ Upload to Replit (2 min)

**Create New Repl:**
- Go to replit.com → Create Repl → Python

**Upload These Files:**
```
bot.py
config.py
keep_alive.py
requirements.txt
.replit
README.md
REPLIT_SETUP.md

database/db_manager.py

handlers/game_handler.py
handlers/lobby_handler.py
handlers/voting_handler.py

models/character.py
models/game.py
models/player.py

services/ai_service.py
services/scoring_service.py
services/team_service.py

utils/constants.py
utils/helpers.py
```

---

### 2️⃣ Configure Secrets (1 min)

Click 🔒 Secrets icon, add:

```
TELEGRAM_BOT_TOKEN = your_bot_token_from_botfather
GEMINI_API_KEY = your_gemini_api_key
LOBBY_SIZE = 9
TEAM_SIZE = 3
ROUND_TIME = 60
REPLIT_DEPLOYMENT = true
```

**Get Keys:**
- Bot Token: [@BotFather](https://t.me/BotFather) → `/newbot`
- Gemini API: [makersuite.google.com](https://makersuite.google.com/app/apikey)

---

### 3️⃣ Run Bot (30 sec)

1. Click "Run" button
2. Wait for "Bot is ready..." in console
3. Check for errors

---

### 4️⃣ Add Characters (1 min)

In Telegram (private chat with bot):
```
/addcharacter
```

Add minimum **12 characters** with:
- Name (English only)
- MBTI (button select)
- Zodiac (button select)
- Password: `Wyatt#9810` or `Yuyalay2000`

---

### 5️⃣ Test Game (30 sec)

In Telegram group:
```
/newgame
```

Click "Join" → Wait for 9 players → Game starts!

---

## 🔄 Keep-Alive (Optional but Recommended)

For free tier to prevent sleep:

1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Create account
3. Add new monitor:
   - Type: HTTP(s)
   - URL: `https://your-repl-name.your-username.repl.co`
   - Interval: 5 minutes
4. Done!

---

## ✅ Verification

### Bot Working?
- [ ] `/start` responds in private chat
- [ ] `/start` responds in group
- [ ] `/newgame` creates lobby

### Game Working?
- [ ] Lobby shows player list
- [ ] Join/quit buttons work
- [ ] Game starts with 9 players
- [ ] Teams announced
- [ ] Voting messages sent

---

## 🐛 Quick Fixes

**Bot not responding?**
```
Check: Secrets → TELEGRAM_BOT_TOKEN
Fix: Get new token from BotFather
```

**Database error?**
```
Check: Repl console for errors
Fix: Click "Run" again (auto-creates database)
```

**Gemini error?**
```
Check: Secrets → GEMINI_API_KEY
Fix: Get key from Google AI Studio
Note: Bot works without AI (uses fallback)
```

**Bot sleeping?**
```
Check: REPLIT_DEPLOYMENT = true
Fix: Setup UptimeRobot monitor
```

---

## 📱 Commands

### Everyone
- `/start` - Welcome
- `/help` - Help info
- `/newgame` - Start game (group)
- `/cancelgame` - Cancel game

### Admins Only
- `/addcharacter` - Add character
  - Password: `Wyatt#9810` or `Yuyalay2000`

---

## 🎮 Game Flow

```
1. /newgame → Lobby created
2. Players join (9 required)
3. Teams formed (3 teams of 3)
4. 5 rounds of voting
5. Winner announced!
```

**Each Round:**
- 4 characters shown
- 60 seconds to vote
- Team chat available
- Best compatibility wins

---

## 📊 Requirements

**Minimum:**
- 12 characters in database
- 9 players to start
- Stable internet

**Recommended:**
- 20-50 characters (variety)
- UptimeRobot (keep-alive)
- Test with 2 players first (set LOBBY_SIZE=2)

---

## 🎉 You're Live!

Bot is running → Add characters → Invite friends → Play!

**Need More Help?**
- Read: `REPLIT_SETUP.md` (detailed guide)
- Check: `DEPLOYMENT_CHECKLIST.md` (step-by-step)
- Review: `README.md` (full documentation)

---

**Have fun! 🎮✨**

