# 🚀 Production Deployment Guide

Bot ကို production environment မှာ deploy လုပ်ဖို့ အဆင့်ဆင့် လမ်းညွှန်ချက်။

---

## ✅ Production-Ready Features

Bot မှာ အောက်ပါ production features တွေ ပါရှိပါပြီ:

- ✅ **Structured Logging** - File rotation with separate error logs
- ✅ **State Management** - Database-backed persistent states
- ✅ **Error Handling** - Graceful error recovery
- ✅ **Database Transactions** - Atomic operations with rollback
- ✅ **Input Validation** - Defensive programming
- ✅ **Health Check Endpoint** - For cloud platform monitoring
- ✅ **Webhook Support** - For production deployments
- ✅ **Clean Logs** - Reduced noise in production mode

---

## 🔧 Pre-Deployment Checklist

### **1. Environment Variables**

`.env` file ဖန်တီးပြီး production values တွေ ထည့်ပါ:

```bash
# Required
TELEGRAM_BOT_TOKEN=your_production_bot_token
DATABASE_URL=postgresql://user:pass@host:port/db
GEMINI_API_KEY=your_gemini_api_key

# Production Settings
WEBHOOK_URL=https://your-app.koyeb.app
WEBHOOK_PATH=/webhook
PORT=8080

# Logging (Production)
LOG_LEVEL=WARNING
ENABLE_CONSOLE_LOGS=true
LOG_DIR=logs
```

### **2. Database Setup**

PostgreSQL database ရှိပြီးသား ဖြစ်ရပါမယ်:

**Options:**
- [Neon](https://neon.tech) - Free PostgreSQL
- [Supabase](https://supabase.com) - Free tier available
- [ElephantSQL](https://www.elephantsql.com) - Free plan
- [Railway](https://railway.app) - PostgreSQL included

### **3. Bot Configuration**

Telegram Bot ကို @BotFather မှာ configure လုပ်ပါ:

```
/setcommands

start - Start the bot
help - Show help information
newgame - Create a new game (admin only)
cancelgame - Cancel current game (admin only)
addcharacter - Add new character (admin only)
```

---

## 🌐 Deployment Platforms

### **Option 1: Koyeb (Recommended)** ⭐

**Why Koyeb:**
- ✅ Free tier available
- ✅ Easy GitHub integration
- ✅ Automatic deployments
- ✅ SSL certificates included
- ✅ Good uptime

**Steps:**
1. Read `KOYEB_DEPLOYMENT.md`
2. Create Koyeb account
3. Connect GitHub repository
4. Configure environment variables
5. Deploy!

**Service URL format:**
```
https://[service-name]-[org-name].koyeb.app
```

### **Option 2: Railway**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

### **Option 3: Render**

1. Connect GitHub repository
2. Choose "Docker"
3. Set environment variables
4. Deploy

### **Option 4: Fly.io**

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Deploy
fly launch
fly deploy
```

---

## 📊 Monitoring & Logs

### **View Logs:**

**Koyeb:**
```
Dashboard → Service → Logs
```

**Railway:**
```bash
railway logs
```

**Render:**
```
Dashboard → Service → Logs
```

### **Log Levels:**

Production မှာ `LOG_LEVEL=WARNING` သုံးပါ:

```bash
# သင်မြင်ရမှာ:
🟢 INFO  - Bot starting up...
🟢 INFO  - Database initialized
🟡 WARNING - Forbidden error (user blocked bot)
🔴 ERROR - Database connection failed
```

### **Log Files:**

Bot က log files ၂ ဖိုင် ဖန်တီးပါတယ်:

```
logs/
├── telegram_bot.log          # All logs
└── telegram_bot_errors.log   # Errors only
```

**Download logs (Koyeb):**
```bash
# Not directly supported - view in dashboard
```

---

## 🔐 Security Best Practices

### **1. Environment Variables**

```bash
# ✅ DO:
- Use environment variables for secrets
- Different tokens for dev/prod
- Rotate API keys regularly

# ❌ DON'T:
- Commit .env to Git
- Share credentials
- Use same tokens everywhere
```

### **2. Database**

```bash
# ✅ DO:
- Use SSL connections
- Backup database regularly
- Limit database user permissions

# ❌ DON'T:
- Use root database user
- Expose database publicly
- Skip backups
```

### **3. Bot Token**

```bash
# If token compromised:
1. Revoke via @BotFather: /revoke
2. Generate new token
3. Update environment variables
4. Redeploy
```

---

## ⚡ Performance Optimization

### **1. Database Connection Pooling**

Already configured in `database/db_manager.py`:

```python
min_size=1      # Minimum connections
max_size=10     # Maximum connections
timeout=30      # Acquisition timeout
```

### **2. Rate Limiting**

Bot က automatic rate limiting ရှိပါပြီ (Telegram API limits):

```
- 30 messages/second per chat
- 20 messages/minute to same user
```

### **3. Memory Management**

```bash
# Recommended resources:
RAM: 512MB minimum
CPU: 1 vCPU minimum
Disk: 1GB minimum
```

---

## 🐛 Troubleshooting

### **Problem 1: Bot not responding**

**Check:**
```bash
1. WEBHOOK_URL is correct
2. Environment variables are set
3. Database is accessible
4. Bot token is valid
```

**Logs should show:**
```
✅ Mode: WEBHOOK
✅ Starting webhook server on port 8080
✅ Database initialized
```

### **Problem 2: Database errors**

**Check:**
```bash
1. DATABASE_URL format is correct
2. Database is running
3. Network connectivity
4. Connection pool not exhausted
```

**Test connection:**
```python
python -c "import asyncpg; import asyncio; asyncio.run(asyncpg.connect('your_database_url'))"
```

### **Problem 3: High memory usage**

**Solutions:**
```bash
1. Reduce MAX_POOL_SIZE in db_manager.py
2. Enable log rotation (already configured)
3. Clear old game data regularly
```

### **Problem 4: Timeout errors**

**Check:**
```bash
1. Network latency
2. Database query performance
3. AI API response time
```

**Increase timeouts if needed in `config.py`**

---

## 📈 Scaling

### **Horizontal Scaling**

⚠️ **Important:** Bot ကို multiple instances မ run ရပါ!

```bash
# ❌ DON'T:
- Run 2+ instances in polling mode
- Run multiple webhook instances

# ✅ DO:
- Use only 1 instance
- Scale database separately
- Use Redis for session storage (future)
```

### **Vertical Scaling**

```bash
# If needed, increase:
- RAM: 512MB → 1GB
- CPU: 1 vCPU → 2 vCPU
```

---

## 🔄 Updates & Maintenance

### **Deploying Updates:**

```bash
# 1. Test locally first
python bot.py

# 2. Commit changes
git add .
git commit -m "Update description"
git push origin main

# 3. Cloud platform auto-deploys (if connected to GitHub)
```

### **Database Migrations:**

```python
# If schema changes needed:
1. Backup database first
2. Update db_manager.py
3. Test migrations locally
4. Deploy to production
```

### **Backup Strategy:**

```bash
# Weekly database backups (automated):
- Use cloud provider's backup feature
- Or setup cron job:
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

---

## 📊 Monitoring Checklist

### **Daily:**
- [ ] Check error logs
- [ ] Monitor uptime
- [ ] Check response times

### **Weekly:**
- [ ] Review database size
- [ ] Check memory usage
- [ ] Review user feedback

### **Monthly:**
- [ ] Backup database
- [ ] Review and clean old data
- [ ] Update dependencies
- [ ] Security audit

---

## 🎯 Performance Metrics

### **Target Metrics:**

```
✅ Uptime: 99.9%
✅ Response time: < 2 seconds
✅ Memory usage: < 512MB
✅ Error rate: < 1%
```

### **Monitoring Tools:**

- **Platform built-in** (Koyeb, Railway, etc.)
- **UptimeRobot** - Free uptime monitoring
- **BetterStack** - Log aggregation
- **Sentry** - Error tracking (optional)

---

## 🚀 Quick Start Commands

### **Deploy to Koyeb:**

```bash
1. Push to GitHub
2. Connect Koyeb to repository
3. Set environment variables
4. Deploy!
```

### **Check Production Logs:**

```bash
# View in platform dashboard
# Or use platform CLI
```

### **Emergency Rollback:**

```bash
# Most platforms support rollback to previous version
# Check platform documentation
```

---

## 📚 Related Documentation

- `KOYEB_DEPLOYMENT.md` - Detailed Koyeb guide
- `CODE_QUALITY_GUIDE.md` - Code best practices
- `ENV_EXAMPLE.md` - Environment variables
- `README.md` - General setup

---

## 🆘 Support

If issues occur:

1. **Check logs first** - Most issues show in logs
2. **Review this guide** - Common problems covered
3. **Check documentation** - Platform-specific guides
4. **Test locally** - Reproduce issue in development

---

## 🎉 Success Indicators

Production deployment အောင်မြင်ရင် မြင်ရမှာ:

```
✅ Bot responds to commands
✅ Games can be created and played
✅ Database operations work
✅ No error spam in logs
✅ Uptime is stable
✅ Memory usage is normal
```

---

**Production ကို အဆင်ပြေပြေနဲ့ deploy လုပ်ပါ! 🚀**

