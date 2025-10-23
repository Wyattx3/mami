# 🐘 PostgreSQL Migration Guide

## ✅ Migration Complete!

The bot has been successfully migrated from **SQLite** to **PostgreSQL (Neon)**.

---

## 📋 What Changed?

### Database Engine
- **Before:** SQLite (local file: `database/game.db`)
- **After:** PostgreSQL hosted on **Neon** (cloud database)

### Benefits of PostgreSQL/Neon
1. ✅ **Cloud-hosted** - Access from anywhere
2. ✅ **Better performance** - For concurrent users
3. ✅ **Scalability** - Handles more players
4. ✅ **Data persistence** - No data loss on Replit restarts
5. ✅ **Free tier** - 0.5 GB storage, sufficient for this bot

---

## 🔐 Environment Setup

### Required: DATABASE_URL

Add this to your `.env` file or Replit Secrets:

```bash
DATABASE_URL=postgresql://neondb_owner:npg_Is20JMRTZhdr@ep-jolly-bush-a15g649l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
```

### Full .env file:

```bash
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Google Gemini AI
GEMINI_API_KEY=your_api_key_here

# PostgreSQL (Neon)
DATABASE_URL=postgresql://neondb_owner:npg_Is20JMRTZhdr@ep-jolly-bush-a15g649l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require

# Admin passwords
ADMIN_PASSWORDS=Wyatt#9810,Yuyalay2000

# Game settings
LOBBY_SIZE=9
TEAM_SIZE=3
ROUND_TIME=180
```

---

## 🚀 Deployment Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**New dependencies:**
- `asyncpg==0.29.0` - PostgreSQL driver
- `psycopg2-binary==2.9.9` - PostgreSQL adapter

**Removed:**
- ~~`aiosqlite`~~ - No longer needed

### 2. Set Environment Variable

**Local development:**
```bash
# Create .env file
echo 'DATABASE_URL=postgresql://...' >> .env
```

**Replit:**
1. Go to **Tools** → **Secrets**
2. Add key: `DATABASE_URL`
3. Value: Your PostgreSQL connection string

### 3. Test Connection

```bash
python test_db_connection.py
```

**Expected output:**
```
✅ Connection pool created successfully!
✅ Database tables created successfully!
✅ Found X characters in database
🎉 All tests passed successfully!
```

### 4. Migrate Existing Data (Optional)

If you have existing characters in SQLite:

```bash
python migrate_to_postgres.py
```

This will copy all characters from `database/game.db` to PostgreSQL.

### 5. Run the Bot

```bash
python bot.py
```

---

## 🗃️ Database Schema

### Tables Created:

1. **characters** - Character database
   - Stores MBTI, Zodiac, personality traits
   
2. **games** - Game sessions
   - Tracks game status, rounds, winners
   
3. **game_players** - Player-game associations
   - Teams, leaders, participants
   
4. **game_rounds** - Round results
   - Votes, selections, scores
   
5. **lobby_queue** - Lobby management
   - Waiting players

---

## 🔄 Key Code Changes

### 1. Database Manager

**Before (SQLite):**
```python
import aiosqlite

async with aiosqlite.connect(self.db_path) as db:
    await db.execute('SELECT * FROM characters WHERE id = ?', (id,))
```

**After (PostgreSQL):**
```python
import asyncpg

async with self.pool.acquire() as conn:
    await conn.fetch('SELECT * FROM characters WHERE id = $1', id)
```

### 2. Connection Pool

**New feature:** Connection pooling for better performance

```python
# Initialize on startup
await db_manager.create_pool()

# Use throughout app lifecycle

# Close on shutdown
await db_manager.close_pool()
```

### 3. Query Syntax

**Placeholders changed:**
- SQLite: `?` → PostgreSQL: `$1, $2, $3`

**Auto-increment:**
- SQLite: `INTEGER PRIMARY KEY AUTOINCREMENT`
- PostgreSQL: `SERIAL PRIMARY KEY`

**Random order:**
- SQLite: `ORDER BY RANDOM()`
- PostgreSQL: `ORDER BY RANDOM()`

---

## 🐛 Troubleshooting

### Error: "no module named 'asyncpg'"

**Fix:**
```bash
pip install asyncpg==0.29.0
```

### Error: "DATABASE_URL must be set"

**Fix:**
Add `DATABASE_URL` to `.env` file or Replit Secrets.

### Error: "connection refused"

**Possible causes:**
1. ❌ Wrong DATABASE_URL
2. ❌ Network/firewall blocking connection
3. ❌ Neon database paused (auto-resumes on connect)

**Test connection:**
```bash
psql 'postgresql://neondb_owner:npg_Is20JMRTZhdr@ep-jolly-bush-a15g649l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
```

### Error: "table already exists"

**Fix:**
This is fine! Tables are created with `CREATE TABLE IF NOT EXISTS`.

---

## 📊 Comparing SQLite vs PostgreSQL

| Feature | SQLite | PostgreSQL (Neon) |
|---------|--------|-------------------|
| **Hosting** | Local file | Cloud-hosted |
| **Concurrent users** | Limited | High performance |
| **Data persistence** | File-based | Always available |
| **Scalability** | Small projects | Production-ready |
| **Cost** | Free | Free tier available |

---

## 🔒 Security Notes

⚠️ **Never commit DATABASE_URL to GitHub!**

- Store in `.env` file (already in `.gitignore`)
- Use Replit Secrets for deployment
- Rotate passwords if exposed

---

## ✅ Verification Checklist

After migration, verify:

- [ ] `requirements.txt` updated
- [ ] `DATABASE_URL` set in environment
- [ ] `python test_db_connection.py` passes
- [ ] Bot starts without errors
- [ ] `/addcharacter` works
- [ ] Game can be created and played
- [ ] No SQLite references in logs

---

## 📁 File Changes Summary

### Modified Files:
- `database/db_manager.py` - Complete rewrite for PostgreSQL
- `bot.py` - Added connection pool initialization
- `config.py` - Added DATABASE_URL configuration
- `requirements.txt` - Updated dependencies

### New Files:
- `test_db_connection.py` - Connection test script
- `migrate_to_postgres.py` - Data migration script
- `POSTGRESQL_MIGRATION.md` - This guide
- `ENV_SETUP.md` - Environment configuration guide

### Removed Dependencies:
- ~~`aiosqlite`~~ - SQLite no longer used

---

## 🎉 Migration Complete!

Your bot now uses PostgreSQL (Neon) for:
- ✅ Better performance
- ✅ Cloud persistence
- ✅ Production scalability
- ✅ Multi-deployment support

**Ready to deploy on Replit!** 🚀

---

**Updated:** October 2025  
**Database:** PostgreSQL (Neon)  
**Commit:** Latest migration

