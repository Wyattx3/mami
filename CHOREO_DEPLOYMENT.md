# 🚀 Choreo.dev Deployment Guide

Complete guide to deploy the Telegram Bot on Choreo.dev platform.

---

## 📋 Prerequisites

1. **Choreo Account:** Sign up at https://console.choreo.dev/
2. **GitHub Account:** Repository must be on GitHub
3. **Bot Token:** From @BotFather on Telegram
4. **Gemini API Key:** From Google AI Studio
5. **PostgreSQL Database:** Neon.tech or similar

---

## 🔧 Step-by-Step Deployment

### 1️⃣ Prepare Repository

**Files needed:**
- ✅ `Dockerfile` - Container configuration
- ✅ `.dockerignore` - Files to exclude from build
- ✅ `requirements.txt` - Python dependencies
- ✅ `.env.template` - Environment variables template

**Push to GitHub:**
```bash
cd "/Users/apple/tele scy"
git add Dockerfile .dockerignore CHOREO_DEPLOYMENT.md
git commit -m "Add Choreo deployment configuration"
git push origin main
```

---

### 2️⃣ Create Choreo Component

1. **Login to Choreo:**
   - Go to https://console.choreo.dev/
   - Sign in with your account

2. **Create New Component:**
   - Click **"+ Create"**
   - Select **"Service"**
   - Choose **"Docker"** as the buildpack

3. **Connect GitHub Repository:**
   - Authorize Choreo to access your GitHub
   - Select repository: `Wyattx3/mami`
   - Branch: `main`
   - Docker context path: `/`
   - Dockerfile path: `Dockerfile`

4. **Configure Component:**
   - Name: `telegram-game-bot`
   - Description: `Telegram Character Matching Game Bot`
   - Port: `8080` (optional, for health checks)

---

### 3️⃣ Configure Environment Variables

In Choreo Console → Your Component → **Configure** → **Environment Variables**:

Add the following:

```env
TELEGRAM_BOT_TOKEN=8265058299:AAESV9okxtDmTu1fIwDsbqTdYkT2_tQRsFI
GEMINI_API_KEY=AIzaSyCgAFHYEpZpXb1Fkyz2BRpYOeENdUfL7ns
DATABASE_URL=postgresql://neondb_owner:npg_Is20JMRTZhdr@ep-jolly-bush-a15g649l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
ADMIN_PASSWORDS=Wyatt#9810,Yuyalay2000
LOBBY_SIZE=9
TEAM_SIZE=3
ROUND_TIME=60
```

**⚠️ Security Note:**
- Mark `TELEGRAM_BOT_TOKEN` as **Secret**
- Mark `GEMINI_API_KEY` as **Secret**
- Mark `DATABASE_URL` as **Secret**
- Mark `ADMIN_PASSWORDS` as **Secret**

---

### 4️⃣ Build and Deploy

1. **Build:**
   - Click **"Build"** in Choreo Console
   - Wait for build to complete (3-5 minutes)
   - Check build logs for any errors

2. **Deploy:**
   - After successful build, click **"Deploy"**
   - Select environment: **"Development"** (for testing)
   - Click **"Deploy"**
   - Wait for deployment (1-2 minutes)

3. **Verify:**
   - Check deployment status: Should show **"Running"**
   - View logs for startup messages:
     ```
     Bot starting up...
     Database connection pool created
     Database initialized
     Application started
     ```

---

### 5️⃣ Test Bot

1. **Open Telegram:**
   - Search for your bot
   - Send `/start` in private chat
   - You should get a welcome message

2. **Test in Group:**
   - Add bot to a group
   - Make bot an admin
   - Send `/newgame`
   - Players can join and game starts

---

## 📊 Monitoring & Logs

### View Logs

**In Choreo Console:**
1. Go to your component
2. Click **"Observability"**
3. Select **"Logs"**
4. Filter by:
   - Time range
   - Log level (INFO, ERROR, etc.)
   - Search keywords

**Useful log searches:**
```
"ERROR"          - Find errors
"Game starting"  - Track game starts
"player joined"  - Monitor lobby activity
"HTTP/1.1 200"   - API success
"HTTP/1.1 409"   - Conflicts (multiple instances)
```

### Metrics

**Track:**
- CPU usage
- Memory usage
- Network traffic
- Request count
- Error rate

**Access:** Choreo Console → Observability → Metrics

---

## 🔄 Updates & Redeploy

### Push Code Updates

```bash
# Make changes locally
cd "/Users/apple/tele scy"

# Test locally
python bot.py

# Commit and push
git add .
git commit -m "Your update description"
git push origin main
```

### Redeploy in Choreo

**Option 1: Auto-deploy (Recommended)**
- Enable auto-deploy in Choreo settings
- Every push to `main` triggers rebuild and redeploy

**Option 2: Manual deploy**
1. Go to Choreo Console
2. Click **"Build"**
3. Wait for build completion
4. Click **"Deploy"**

---

## 🔧 Troubleshooting

### Build Fails

**Check:**
1. `Dockerfile` syntax
2. `requirements.txt` dependencies
3. Build logs in Choreo Console

**Common issues:**
```bash
# Missing dependencies
RUN apt-get update && apt-get install -y gcc g++

# Python version mismatch
FROM python:3.12-slim  # Match your local version

# Permission errors
RUN chown -R botuser:botuser /app
```

### Deployment Fails

**Check:**
1. Environment variables are set correctly
2. All required secrets are added
3. Database connection string is valid

**Test database connection:**
```bash
# In Choreo logs, look for:
"Database connection pool created"
"Database initialized successfully"
```

### Bot Not Responding

**Check:**
1. Deployment status is "Running"
2. No errors in logs
3. Bot token is correct
4. No other bot instances running

**Conflict error:**
```
Conflict: terminated by other getUpdates request
```
**Solution:** Stop other bot instances (Replit, local, etc.)

### Database Connection Issues

**Check:**
1. `DATABASE_URL` is correct
2. Neon database is active
3. IP whitelist (Neon allows all by default)

**Test:**
```bash
# Look for in logs:
"Creating database connection pool..."
"Database connection pool created"
```

---

## 🔐 Security Best Practices

### Environment Variables

✅ **DO:**
- Use Choreo's secret management
- Rotate tokens periodically
- Use different tokens for dev/prod

❌ **DON'T:**
- Commit `.env` to Git
- Share tokens publicly
- Use same token across platforms

### Database

✅ **DO:**
- Use SSL connections (`sslmode=require`)
- Regular backups
- Monitor for unusual activity

❌ **DON'T:**
- Expose database publicly
- Use weak passwords
- Skip connection pooling

---

## 📈 Scaling

### Horizontal Scaling

**Choreo supports:**
- Multiple replicas
- Load balancing
- Auto-scaling

**⚠️ Important for Telegram Bots:**
> You **CANNOT** run multiple instances of the same bot!
> Telegram only allows one `getUpdates` connection per token.

**Solutions:**
1. Use **webhook mode** instead of polling
2. Run only **1 replica**
3. Use Choreo's health checks for restart

### Vertical Scaling

**Adjust resources:**
- CPU: 1-2 cores recommended
- Memory: 512MB - 1GB
- Disk: Minimal (database is external)

---

## 💰 Cost Estimation

**Choreo Free Tier:**
- ✅ Good for development
- ✅ Limited resources
- ✅ Community support

**Paid Tiers:**
- Production-ready
- 24/7 uptime
- Advanced monitoring
- Priority support

**Comparison:**

| Platform | Free Tier | Uptime | Ease |
|----------|-----------|--------|------|
| Choreo   | Yes       | High   | Easy |
| Replit   | Yes       | Medium | Easy |
| Heroku   | No*       | High   | Medium |
| Railway  | Limited   | High   | Easy |

---

## 🔄 Migration from Replit

### Stop Replit Bot

```bash
# In Replit, stop the running process
# Or delete the deployment
```

### Deploy to Choreo

Follow steps 1-5 above

### Verify

```bash
# Check Telegram bot responds
# Check database is accessible
# Check logs for errors
```

### Update DNS (if using custom domain)

Point your domain to Choreo endpoint

---

## 📞 Support

### Choreo Support

- **Docs:** https://wso2.com/choreo/docs/
- **Community:** https://discord.gg/wso2
- **Issues:** https://github.com/wso2/choreo-samples

### Bot Issues

- **GitHub:** https://github.com/Wyattx3/mami/issues
- **Logs:** Check Choreo Console → Observability

---

## ✅ Deployment Checklist

Before going live:

- [ ] Dockerfile tested locally
- [ ] Environment variables configured
- [ ] Database connection verified
- [ ] Bot token is valid
- [ ] Gemini API key is valid
- [ ] Build successful in Choreo
- [ ] Deployment successful
- [ ] Bot responds to `/start`
- [ ] Game creation works
- [ ] No errors in logs
- [ ] Monitoring enabled
- [ ] Backup plan ready

---

## 🎯 Quick Commands

```bash
# Local testing
docker build -t telegram-bot .
docker run --env-file .env telegram-bot

# Git updates
git add .
git commit -m "Update message"
git push origin main

# Check logs (Choreo CLI if available)
choreo logs --component telegram-game-bot --follow
```

---

## 🚀 Production Ready!

Once deployed successfully on Choreo:

✅ **24/7 Uptime**  
✅ **Auto-restart on failure**  
✅ **Monitoring & logs**  
✅ **Scalable infrastructure**  
✅ **Professional deployment**  

Your bot is now production-ready! 🎉

---

**Last Updated:** October 23, 2025  
**Platform:** Choreo.dev  
**Status:** Production Ready

