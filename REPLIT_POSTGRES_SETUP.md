# 🚀 Replit Setup with PostgreSQL (Neon)

## ✅ Quick Start - PostgreSQL Version

The bot now uses **PostgreSQL (Neon)** instead of SQLite for better performance and data persistence!

---

## 📋 Step-by-Step Setup

### 1. Pull Latest Code

**In Replit Shell:**
```bash
git pull origin main
```

**Expected output:**
```
Updating 181678c..fbccf14
Fast-forward
 10 files changed, 786 insertions(+), 190 deletions(-)
```

---

### 2. Install New Dependencies

**In Replit Shell:**
```bash
pip install -r requirements.txt
```

**New packages installed:**
- `asyncpg==0.29.0` - PostgreSQL async driver
- `psycopg2-binary==2.9.9` - PostgreSQL adapter

**Removed:**
- ~~`aiosqlite`~~ - No longer needed

---

### 3. Configure Secrets

**Go to: Tools → Secrets**

Add these keys:

| Key | Value |
|-----|-------|
| `TELEGRAM_BOT_TOKEN` | Your bot token |
| `GEMINI_API_KEY` | Your Gemini API key |
| `DATABASE_URL` | `postgresql://neondb_owner:npg_Is20JMRTZhdr@ep-jolly-bush-a15g649l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require` |
| `ADMIN_PASSWORDS` | `Wyatt#9810,Yuyalay2000` |
| `LOBBY_SIZE` | `9` |
| `TEAM_SIZE` | `3` |
| `ROUND_TIME` | `180` |

---

### 4. Test Database Connection

**Before running the bot, test the connection:**

```bash
python test_db_connection.py
```

**Success output:**
```
✅ Connection pool created successfully!
✅ Database tables created successfully!
✅ Found X characters in database
🎉 All tests passed successfully!
```

**If errors occur:**
- Check `DATABASE_URL` in Secrets
- Verify Neon database is accessible
- Run: `pip install asyncpg psycopg2-binary`

---

### 5. Migrate Existing Data (Optional)

**If you have characters in old SQLite database:**

```bash
python migrate_to_postgres.py
```

**When prompted, type:** `yes`

This will copy all characters from SQLite to PostgreSQL.

---

### 6. Run the Bot

**Click the "Run" button** or:

```bash
python bot.py
```

**Expected output:**
```
==================================================
Bot starting up...
==================================================
🔌 Creating connection pool...
✅ Database connection pool created
📋 Creating database tables...
✅ Database initialized successfully
🎮 Setting up handlers...
✅ All handlers registered successfully
🤖 Bot is ready and starting to poll...
==================================================
```

---

## 🎯 Verification Steps

### 1. Bot Starts Successfully
- ✅ No errors in console
- ✅ "Bot is ready and starting to poll..." message appears

### 2. Database Connection Works
- ✅ "Database connection pool created" in logs
- ✅ "Database initialized successfully" in logs

### 3. Commands Work
**In Telegram:**
- `/start` - Should show welcome message
- `/addcharacter` - Should allow adding characters
- `/newgame` - Should create game lobby in group

### 4. Game Functions
- ✅ Players can join lobby
- ✅ Game starts with 9 players
- ✅ Teams are assigned
- ✅ Voting works
- ✅ Results are displayed

---

## 🐛 Troubleshooting

### Error: "DATABASE_URL must be set"

**Fix:**
Add `DATABASE_URL` to Replit Secrets (see Step 3).

---

### Error: "ModuleNotFoundError: No module named 'asyncpg'"

**Fix:**
```bash
pip install asyncpg==0.29.0 psycopg2-binary==2.9.9
```

---

### Error: "connection refused" or "timeout"

**Possible causes:**
1. Wrong DATABASE_URL
2. Neon database paused (auto-resumes on connect)
3. Network issue

**Fix:**
Test with psql:
```bash
psql 'postgresql://neondb_owner:npg_Is20JMRTZhdr@ep-jolly-bush-a15g649l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
```

---

### Error: "table game_players has no column named is_leader"

**This should NOT happen with PostgreSQL migration!**

But if it does:
```bash
# The migration creates tables from scratch
# No need for ALTER TABLE
```

---

### Error: "ImportError: cannot import name 'AcceptedGiftTypes'"

**Fix:**
```bash
pip install python-telegram-bot==21.5 --force-reinstall
```

---

## 🔄 Fresh Start (Nuclear Option)

**If nothing works:**

```bash
# 1. Stop bot
# 2. In Shell:

# Delete Python cache
rm -rf .pythonlibs
rm -rf __pycache__
find . -name "*.pyc" -delete

# Pull latest code
git pull origin main

# Clean install
pip cache purge
pip install -r requirements.txt

# Test connection
python test_db_connection.py

# Run bot
python bot.py
```

---

## 📊 What's Different from SQLite?

| Aspect | SQLite (Old) | PostgreSQL (New) |
|--------|--------------|------------------|
| **Database file** | `database/game.db` | Cloud-hosted on Neon |
| **Data persistence** | Lost on Replit restart | Always persisted |
| **Connection** | File path | Connection URL |
| **Performance** | Limited concurrency | High performance |
| **Deployment** | File must exist | Auto-creates on connect |

---

## ✅ Success Indicators

After setup, you should see:

**Console:**
```
✅ Database connection pool created
✅ Database initialized successfully
✅ Bot is ready and starting to poll...
```

**Telegram:**
```
/start → Shows welcome message
/addcharacter → Allows adding characters
/newgame → Creates game lobby
```

**No errors like:**
```
❌ DATABASE_URL must be set
❌ ModuleNotFoundError: asyncpg
❌ Connection refused
❌ Table does not exist
```

---

## 📚 Additional Resources

- **Full Migration Guide:** `POSTGRESQL_MIGRATION.md`
- **Environment Setup:** `ENV_SETUP.md`
- **Library Fix:** `REPLIT_LIBRARY_FIX.md`
- **Database Update:** `REPLIT_UPDATE_GUIDE.md`

---

## 🎉 Ready to Deploy!

Once you see:
```
🤖 Bot is ready and starting to poll...
```

Your bot is live and using PostgreSQL! 🚀

---

**Key Benefits:**
- ✅ Data persists across Replit restarts
- ✅ Better performance for multiple users
- ✅ Production-ready database
- ✅ Free Neon tier (0.5 GB)

---

**Updated:** October 2025  
**Database:** PostgreSQL (Neon)  
**Commit:** fbccf14 - PostgreSQL Migration

