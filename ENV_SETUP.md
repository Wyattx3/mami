# 🔐 Environment Variables Setup

## Required Environment Variables

Create a `.env` file in the project root with these values:

```bash
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Google Gemini AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Admin Passwords (comma-separated)
ADMIN_PASSWORDS=Wyatt#9810,Yuyalay2000

# PostgreSQL Database Configuration (Neon)
DATABASE_URL=postgresql://neondb_owner:npg_Is20JMRTZhdr@ep-jolly-bush-a15g649l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require

# Game Configuration
LOBBY_SIZE=9
TEAM_SIZE=3
ROUND_TIME=180
```

---

## Replit Secrets Setup

If deploying on Replit, add these as **Secrets** (not in .env file):

1. Go to **Tools** → **Secrets**
2. Add each variable:

| Key | Value |
|-----|-------|
| `TELEGRAM_BOT_TOKEN` | Your bot token from @BotFather |
| `GEMINI_API_KEY` | Your Gemini API key |
| `ADMIN_PASSWORDS` | `Wyatt#9810,Yuyalay2000` |
| `DATABASE_URL` | `postgresql://neondb_owner:npg_Is20JMRTZhdr@ep-jolly-bush-a15g649l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require` |
| `LOBBY_SIZE` | `9` |
| `TEAM_SIZE` | `3` |
| `ROUND_TIME` | `180` |

---

## Database URL Format

```
postgresql://[user]:[password]@[host]/[database]?sslmode=require
```

**Your Neon Database:**
- **User:** `neondb_owner`
- **Password:** `npg_Is20JMRTZhdr`
- **Host:** `ep-jolly-bush-a15g649l-pooler.ap-southeast-1.aws.neon.tech`
- **Database:** `neondb`
- **SSL:** Required

---

## Testing Connection

To test database connection:

```bash
python test_db_connection.py
```

---

## Security Notes

⚠️ **Never commit .env file to GitHub!**

- `.env` is already in `.gitignore`
- Use Replit Secrets for sensitive data
- Rotate passwords if exposed

---

**Updated:** October 2025  
**Database:** PostgreSQL (Neon)

