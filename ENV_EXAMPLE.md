# 🔧 Environment Variables Configuration

ဒီ file က `.env` file အတွက် example configuration ဖြစ်ပါတယ်။

---

## 📝 Production Configuration (Koyeb/Cloud)

`.env` file ဖန်တီးပြီး အောက်ပါ variables တွေ ထည့်ပါ:

```bash
# ==================== Required ====================

# Telegram Bot Token
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Database URL (PostgreSQL)
DATABASE_URL=postgresql://user:password@host:port/database

# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here


# ==================== Production Settings ====================

# Webhook Mode (for cloud deployment)
WEBHOOK_URL=https://your-app.koyeb.app
WEBHOOK_PATH=/webhook
PORT=8080

# Logging (Production)
LOG_LEVEL=WARNING
LOG_DIR=logs
ENABLE_CONSOLE_LOGS=true


# ==================== Game Settings ====================

LOBBY_SIZE=9
TEAM_SIZE=3
ROUND_TIME=60
```

---

## 🖥️ Development Configuration (Local)

```bash
# ==================== Required ====================

TELEGRAM_BOT_TOKEN=your_bot_token_here
DATABASE_URL=postgresql://user:password@host:port/database
GEMINI_API_KEY=your_gemini_api_key_here


# ==================== Development Settings ====================

# Polling Mode (leave WEBHOOK_URL empty)
WEBHOOK_URL=
PORT=8080

# Logging (Development)
LOG_LEVEL=INFO
LOG_DIR=logs
ENABLE_CONSOLE_LOGS=true


# ==================== Game Settings ====================

LOBBY_SIZE=9
TEAM_SIZE=3
ROUND_TIME=60
```

---

## 📊 Log Levels အကြောင်း:

| Level | Usage | Description |
|-------|-------|-------------|
| **DEBUG** | Development only | အသေးစိတ် debugging info အားလုံး |
| **INFO** | Development | Normal operations logs |
| **WARNING** | Production ⭐ | Warnings only (recommended) |
| **ERROR** | Production | Errors only |
| **CRITICAL** | Production | Critical failures only |

---

## 🚀 Quick Setup:

### **1. Create `.env` file:**
```bash
touch .env
```

### **2. Copy configuration:**

**For Production:**
```bash
cp ENV_EXAMPLE.md .env
# Then edit with production values and set LOG_LEVEL=WARNING
```

**For Development:**
```bash
cp ENV_EXAMPLE.md .env
# Then edit with development values and set LOG_LEVEL=INFO
```

### **3. Edit values:**
```bash
nano .env
# or
code .env
```

---

## ⚠️ Important Notes:

1. ✅ **Never commit `.env` to Git** - It contains secrets!
2. ✅ **Use WARNING level in production** - Reduces log noise
3. ✅ **Use INFO level in development** - Easier debugging
4. ✅ **Set WEBHOOK_URL only for cloud deployment** - Local uses polling
5. ✅ **Keep backups of your `.env` file** - Store securely

---

## 🔐 Security Best Practices:

- ✅ Never share your `.env` file
- ✅ Use different bot tokens for dev/prod
- ✅ Rotate API keys regularly
- ✅ Use environment variables in CI/CD
- ✅ Keep database credentials secure

---

## 📚 Related Documentation:

- `KOYEB_DEPLOYMENT.md` - Deploy to Koyeb
- `CODE_QUALITY_GUIDE.md` - Code best practices
- `README.md` - General setup guide

---

**Happy Coding! 🎉**

