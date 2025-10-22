# 📋 Replit Deployment Checklist

## ✅ Pre-Deployment

- [ ] Have Telegram Bot Token from @BotFather
- [ ] Have Gemini API Key from Google AI Studio
- [ ] Verified bot works locally
- [ ] Have at least 12 characters in database (or ready to add)

---

## 📦 Files to Upload to Replit

### Core Files
- [ ] `bot.py` - Main bot file
- [ ] `config.py` - Configuration
- [ ] `keep_alive.py` - Keep-alive server
- [ ] `requirements.txt` - Dependencies
- [ ] `.replit` - Replit configuration
- [ ] `README.md` - Documentation
- [ ] `REPLIT_SETUP.md` - Setup guide

### Database Module
- [ ] `database/` folder
- [ ] `database/__init__.py` (if exists)
- [ ] `database/db_manager.py`

### Handlers Module
- [ ] `handlers/` folder
- [ ] `handlers/__init__.py` (if exists)
- [ ] `handlers/game_handler.py`
- [ ] `handlers/lobby_handler.py`
- [ ] `handlers/voting_handler.py`

### Models Module
- [ ] `models/` folder
- [ ] `models/__init__.py` (if exists)
- [ ] `models/character.py`
- [ ] `models/player.py`
- [ ] `models/game.py`

### Services Module
- [ ] `services/` folder
- [ ] `services/__init__.py` (if exists)
- [ ] `services/ai_service.py`
- [ ] `services/scoring_service.py`
- [ ] `services/team_service.py`

### Utils Module
- [ ] `utils/` folder
- [ ] `utils/__init__.py` (if exists)
- [ ] `utils/constants.py`
- [ ] `utils/helpers.py`

### DO NOT Upload
- [ ] ❌ `.env` file (use Replit Secrets instead)
- [ ] ❌ `venv/` folder
- [ ] ❌ `__pycache__/` folders
- [ ] ❌ `*.db` files (will be created automatically)
- [ ] ❌ `.DS_Store`, `*.log` files

---

## ⚙️ Replit Configuration

### 1. Environment Secrets
In Replit Secrets panel, add:

```
Key: TELEGRAM_BOT_TOKEN
Value: your_actual_bot_token_here
```

```
Key: GEMINI_API_KEY
Value: your_actual_gemini_api_key_here
```

```
Key: LOBBY_SIZE
Value: 9
```

```
Key: TEAM_SIZE
Value: 3
```

```
Key: ROUND_TIME
Value: 60
```

```
Key: REPLIT_DEPLOYMENT
Value: true
```

### 2. Verify Secrets
- [ ] All 6 secrets added
- [ ] No typos in keys
- [ ] Correct values entered
- [ ] Bot token starts with number
- [ ] API key is valid

---

## 🚀 Deployment Steps

### Step 1: Create Repl
- [ ] Go to replit.com
- [ ] Click "Create Repl"
- [ ] Choose Python
- [ ] Name it (e.g., "telegram-strategy-game")

### Step 2: Upload Files
- [ ] Upload all files from checklist above
- [ ] Verify folder structure is correct
- [ ] Check all Python files uploaded

### Step 3: Configure Secrets
- [ ] Open Secrets panel (lock icon)
- [ ] Add all 6 environment variables
- [ ] Verify values are correct

### Step 4: Test Run
- [ ] Click "Run" button
- [ ] Check console for "Bot started" message
- [ ] Verify no errors in logs
- [ ] Test bot in Telegram private chat

### Step 5: Add Characters
- [ ] Use `/addcharacter` in private chat
- [ ] Add minimum 12 characters
- [ ] Use admin password when prompted
- [ ] Verify characters saved

### Step 6: Test Game
- [ ] Add bot to test group
- [ ] Use `/newgame` command
- [ ] Join with test accounts (or set LOBBY_SIZE=2 for testing)
- [ ] Complete one full game
- [ ] Verify scoring works

---

## 🔄 Keep-Alive Setup (Free Tier)

### Step 1: Get Repl URL
- [ ] Note your Repl URL: `https://your-repl-name.your-username.repl.co`
- [ ] Test URL in browser (should show "Bot is running! 🤖")

### Step 2: Setup UptimeRobot
- [ ] Go to uptimerobot.com
- [ ] Create free account
- [ ] Click "Add New Monitor"
- [ ] Type: HTTP(s)
- [ ] Name: "Telegram Bot"
- [ ] URL: Your Repl URL
- [ ] Interval: 5 minutes
- [ ] Click "Create Monitor"

### Step 3: Verify Keep-Alive
- [ ] Check Repl stays awake
- [ ] Monitor shows "Up" status
- [ ] Bot responds in Telegram

---

## ✅ Post-Deployment Verification

### Bot Health
- [ ] Bot responds to `/start` in private chat
- [ ] Bot responds to `/start` in group chat
- [ ] `/newgame` works in group
- [ ] `/addcharacter` works with correct password
- [ ] `/help` shows correct information

### Game Functionality
- [ ] Lobby system works (join/quit)
- [ ] Game starts with correct player count
- [ ] Teams formed correctly
- [ ] Leaders assigned randomly
- [ ] Round messages sent
- [ ] Voting works in private chat
- [ ] Team chat works
- [ ] Scoring calculates correctly
- [ ] Winner announced

### Database
- [ ] Characters saved correctly
- [ ] Games created in database
- [ ] Players recorded
- [ ] Round results saved
- [ ] No database errors in logs

---

## 🐛 Troubleshooting Checklist

### Bot Not Starting
- [ ] Check Secrets are set correctly
- [ ] Verify bot token is valid
- [ ] Check console for error messages
- [ ] Verify all files uploaded

### Bot Not Responding
- [ ] Check bot is running in Repl
- [ ] Verify webhook is deleted
- [ ] Check bot token in BotFather
- [ ] Test in private chat first

### Database Errors
- [ ] Check database folder exists
- [ ] Verify write permissions
- [ ] Delete and recreate database
- [ ] Check file paths in config

### Gemini API Errors
- [ ] Verify API key is correct
- [ ] Check quota limits
- [ ] Test API key in Google AI Studio
- [ ] Bot should use fallback descriptions

### Keep-Alive Not Working
- [ ] Verify REPLIT_DEPLOYMENT=true
- [ ] Check Flask is installed
- [ ] Test Repl URL in browser
- [ ] Verify UptimeRobot monitor is active

---

## 📊 Production Checklist

### Before Going Live
- [ ] Test with 9 real players
- [ ] Verify all rounds work
- [ ] Test scoring accuracy
- [ ] Check character variety (20+ recommended)
- [ ] Test cancellation feature
- [ ] Verify admin commands work

### Monitoring
- [ ] Setup UptimeRobot monitoring
- [ ] Check logs regularly
- [ ] Monitor database size
- [ ] Watch for API rate limits

### Maintenance
- [ ] Backup database regularly
- [ ] Add new characters periodically
- [ ] Monitor error logs
- [ ] Update dependencies if needed

---

## 🎉 Launch Ready!

Once all items are checked:
- ✅ Bot is deployed on Replit
- ✅ Keep-alive is configured
- ✅ Characters are loaded
- ✅ Game tested successfully

**Your Telegram Strategy Game is LIVE!** 🚀

---

**Need Help?**
- Check REPLIT_SETUP.md for detailed instructions
- Review bot logs in Repl console
- Test commands in private chat first
- Verify all Secrets are set correctly

**Good luck and have fun!** 🎮

