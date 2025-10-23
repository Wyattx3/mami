# 🖥️ Local Development Setup

## ✅ Complete Local Setup Guide

**For:** Running bot on your local machine (macOS/Linux/Windows)

---

## 📋 Prerequisites

1. **Python 3.10+** installed
2. **Git** installed
3. **Telegram Bot Token** from @BotFather
4. **Google Gemini API Key** from Google AI Studio

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
cd "/Users/apple/tele scy"
# Already cloned!
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

**Create `.env` file:**
```bash
# Copy from template
cp .env.template .env

# Edit with your values
nano .env  # or use any text editor
```

**Required variables in `.env`:**
```bash
# Telegram Bot (Get from @BotFather)
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Gemini AI (Get from https://makersuite.google.com/app/apikey)
GEMINI_API_KEY=your_api_key_here

# PostgreSQL Database (Neon - already configured)
DATABASE_URL=postgresql://neondb_owner:npg_Is20JMRTZhdr@ep-jolly-bush-a15g649l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require

# Admin passwords
ADMIN_PASSWORDS=Wyatt#9810,Yuyalay2000

# Game settings
LOBBY_SIZE=9
TEAM_SIZE=3
ROUND_TIME=180
```

### 5. Test Database Connection
```bash
python3 test_db_connection.py
```

**Expected output:**
```
✅ Connection pool created successfully!
✅ Database tables created successfully!
✅ Found 43 characters in database
🎉 All tests passed successfully!
```

### 6. Run Bot
```bash
python bot.py
```

**Expected output:**
```
==================================================
Bot starting up...
==================================================
✅ Database connection pool created
✅ Database initialized successfully
🎮 Setting up handlers...
✅ All handlers registered successfully
🤖 Bot is ready and starting to poll...
==================================================
```

---

## 🔐 Getting API Keys

### Telegram Bot Token

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Follow instructions to name your bot
4. Copy the token provided
5. Add to `.env`: `TELEGRAM_BOT_TOKEN=your_token_here`

### Google Gemini API Key

1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Add to `.env`: `GEMINI_API_KEY=your_key_here`

---

## 📁 File Structure

```
tele scy/
├── .env                    # Your environment variables (DO NOT COMMIT)
├── .env.template          # Template for .env
├── .gitignore             # Git ignore file (.env is ignored)
├── bot.py                 # Main bot entry point
├── config.py              # Configuration loader
├── requirements.txt       # Python dependencies
├── database/
│   ├── db_manager.py      # Database operations
│   └── __init__.py
├── handlers/
│   ├── game_handler.py
│   ├── lobby_handler.py
│   ├── voting_handler.py
│   └── __init__.py
├── models/
│   ├── character.py
│   ├── game.py
│   └── __init__.py
├── services/
│   ├── ai_service.py
│   ├── scoring_service.py
│   └── team_service.py
└── utils/
    ├── helpers.py
    └── constants.py
```

---

## 🧪 Testing

### Run All Tests
```bash
# Comprehensive bot test
python3 test_bot_features.py

# Private message test (50 players)
python3 test_private_messages.py

# Team voting test (9 players)
python3 test_team_voting.py

# Database connection test
python3 test_db_connection.py
```

### Expected Results
```
✅ All tests should pass
✅ No errors in console
✅ Database connected
✅ Characters loaded
```

---

## 🐛 Troubleshooting

### Error: "DATABASE_URL must be set"

**Problem:** `.env` file missing or incomplete

**Solution:**
```bash
# Check if .env exists
ls -la .env

# If missing, create it
cp .env.template .env

# Edit with your values
nano .env
```

### Error: "ModuleNotFoundError: No module named 'telegram'"

**Problem:** Dependencies not installed

**Solution:**
```bash
# Make sure venv is activated
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Error: "Connection refused" (Database)

**Problem:** Network issues or wrong DATABASE_URL

**Solution:**
```bash
# Test with psql
psql 'postgresql://neondb_owner:npg_Is20JMRTZhdr@...'

# Check DATABASE_URL in .env
cat .env | grep DATABASE_URL
```

### Error: "Invalid token" (Telegram)

**Problem:** Wrong TELEGRAM_BOT_TOKEN

**Solution:**
```bash
# Get new token from @BotFather
# Update in .env
TELEGRAM_BOT_TOKEN=your_correct_token_here
```

### Bot starts but doesn't respond

**Problem:** Bot not added to group or commands not registered

**Solution:**
1. Add bot to Telegram group
2. Make bot an admin
3. Send `/start` in group
4. Check bot console for errors

---

## 📊 Monitoring

### Check Bot Status
```bash
# View logs
tail -f bot.log  # if logging to file

# Or watch console
python bot.py
```

### Check Database
```bash
# Quick test
python3 test_db_connection.py

# Or connect directly
psql 'postgresql://...'
```

---

## 🔄 Updating

### Pull Latest Changes
```bash
git pull origin main
```

### Update Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Restart Bot
```bash
# Stop current bot (Ctrl+C)
# Start again
python bot.py
```

---

## 🚦 Environment Variables Reference

### Required
```bash
TELEGRAM_BOT_TOKEN       # Telegram bot token from @BotFather
GEMINI_API_KEY          # Google Gemini API key
DATABASE_URL            # PostgreSQL connection string
```

### Optional
```bash
ADMIN_PASSWORDS         # Comma-separated admin passwords (default: Wyatt#9810,Yuyalay2000)
LOBBY_SIZE             # Players per game (default: 9)
TEAM_SIZE              # Players per team (default: 3)
ROUND_TIME             # Seconds per round (default: 180)
```

---

## 💡 Development Tips

### Running in Background
```bash
# macOS/Linux
nohup python bot.py > bot.log 2>&1 &

# Check process
ps aux | grep bot.py

# Stop
kill <process_id>
```

### Auto-restart on Crash
```bash
# Using while loop
while true; do
    python bot.py
    echo "Bot crashed, restarting in 5 seconds..."
    sleep 5
done
```

### Debug Mode
```python
# In config.py or bot.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📚 Additional Resources

### Documentation
- `README.md` - Project overview
- `POSTGRESQL_MIGRATION.md` - Database migration guide
- `PUBLIC_BOT_READINESS.md` - Production readiness
- `VOTING_SYSTEM_TEST_RESULTS.md` - Voting tests

### Test Scripts
- `test_bot_features.py` - Comprehensive tests
- `test_private_messages.py` - Message delivery
- `test_team_voting.py` - Voting system
- `test_db_connection.py` - Database check

---

## ✅ Verification Checklist

Before running bot:
- [ ] `.env` file created with all variables
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Database connection tested
- [ ] Telegram bot token valid
- [ ] Gemini API key valid

After starting bot:
- [ ] No errors in console
- [ ] "Bot is ready and starting to poll..." message
- [ ] Bot responds to `/start` in Telegram
- [ ] Bot added to test group
- [ ] Bot is admin in group

---

## 🎯 Quick Commands Reference

```bash
# Activate venv
source venv/bin/activate

# Install deps
pip install -r requirements.txt

# Test DB
python3 test_db_connection.py

# Run bot
python bot.py

# Run tests
python3 test_bot_features.py

# Deactivate venv
deactivate
```

---

## 🚀 Ready to Run!

Once `.env` is configured:

```bash
source venv/bin/activate
python bot.py
```

You should see:
```
🤖 Bot is ready and starting to poll...
```

**Then test in Telegram:**
1. Private chat: `/start`
2. Add to group
3. In group: `/newgame`
4. Players join
5. Game starts!

---

**Status:** ✅ Ready for local development

**Need help?** Check the documentation files or run test scripts!


