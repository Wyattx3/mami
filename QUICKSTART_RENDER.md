# 🚀 Quick Start: Render Deployment

Render API Key ပါပြီး automatic deployment လုပ်ဖို့ လမ်းညွှန်

## ⚡ အမြန် Deploy လုပ်နည်း

### Option 1: Automatic Script (အကြံပြု)

```bash
# Step 1: GitHub မှာ code upload
./github_setup.sh

# Step 2: Render မှာ deploy
python3 deploy_to_render.py
```

### Option 2: Manual Steps

#### 1️⃣ GitHub Repository ဖန်တီးပါ

```bash
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit for Render"

# Set branch
git branch -M main

# Add remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push
git push -u origin main
```

**GitHub repo မရှိသေးရင်:**
1. https://github.com/new သို့ သွားပါ
2. Repository name: `telegram-strategy-game`
3. Public ရွေးပါ
4. Create repository
5. URL copy လုပ်ပါ

#### 2️⃣ Render မှာ Deploy

**Option A: Automatic Script**

```bash
python3 deploy_to_render.py
```

Script က automatic လုပ်ပေးမယ်:
- ✅ Render account ကို connect လုပ်မယ်
- ✅ Service ဖန်တီးမယ်
- ✅ Environment variables set လုပ်မယ်
- ✅ Deployment start လုပ်မယ်

**Option B: Manual Dashboard**

1. **Render Dashboard:** https://dashboard.render.com/
2. **New +** → **Background Worker**
3. **Connect Repository:**
   - GitHub သို့မဟုတ် GitLab ရွေးပါ
   - Repository ရှာပြီး ရွေးပါ
4. **Configure:**
   - Name: `telegram-strategy-game-bot`
   - Runtime: `Python 3`
   - Build: `pip install -r requirements.txt`
   - Start: `python bot.py`
5. **Environment Variables:**
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token
   GEMINI_API_KEY=your_gemini_key
   LOBBY_SIZE=9
   TEAM_SIZE=3
   ROUND_TIME=60
   ```
6. **Create Background Worker**

## 📋 လိုအပ်တဲ့ API Keys

### 1. Telegram Bot Token
```bash
# BotFather မှာ ရယူပါ
1. Telegram မှာ @BotFather ရှာပါ
2. /newbot ပို့ပါ
3. Bot name နဲ့ username ပေးပါ
4. Token copy လုပ်ပါ
```

### 2. Gemini API Key
```bash
# Google AI Studio မှာ ရယူပါ
1. https://makersuite.google.com/app/apikey
2. Create API key
3. Copy လုပ်ပါ
```

### 3. Render API Key (ရှိပြီးသား)
```
rnd_uAdpSqV7J9Fj4lZEKDQ6SXSaOXpJ
```

## 🔍 Deployment စစ်ဆေးခြင်း

### 1. Logs ကြည့်ပါ

**Via Dashboard:**
```
https://dashboard.render.com/ → Services → Your Bot → Logs
```

**လိုချင်တဲ့ messages:**
```
Bot starting up...
Database initialized
Bot is ready and starting to poll for updates...
```

### 2. Bot စမ်းကြည့်ပါ

```
1. Telegram မှာ bot ကို ရှာပါ
2. /start ပို့ပါ
3. Response ပြန်လာရင် success! ✅
```

### 3. Characters ထည့်ပါ

```
1. /addcharacter command သုံးပါ
2. အနည်းဆုံး 12 characters ထည့်ပါ
3. Admin password: Wyatt#9810 သို့မဟုတ် Yuyalay2000
```

## ⚠️ အဖြစ်များတဲ့ ပြဿနာများ

### ❌ "Repository not found"
```bash
# Solution: GitHub repo ကို public လုပ်ထားမလား စစ်ပါ
# သို့မဟုတ် Render ကို GitHub access ပေးထားမလား စစ်ပါ
```

### ❌ "Build failed"
```bash
# Solution: requirements.txt မှန်ကန်မှု စစ်ပါ
# Python version စစ်ပါ (3.8+)
```

### ❌ "Bot not responding"
```bash
# Solution:
# 1. Environment variables မှန်ကန်မလား စစ်ပါ
# 2. Bot token valid ဖြစ်မလား စစ်ပါ
# 3. Logs မှာ errors ကြည့်ပါ
```

### ❌ "Database errors"
```bash
# Solution: Persistent disk add လုပ်ပါ
# Dashboard → Settings → Disks → Add Disk
# Mount path: /opt/render/project/src/database
```

## 📊 Monitoring

### Dashboard Links
```
Main Dashboard: https://dashboard.render.com/
Services: https://dashboard.render.com/services
Logs: https://dashboard.render.com/[service-id]/logs
```

### Service Status
- 🟢 **Live** - Running ပုံမှန်
- 🟡 **Building** - Deploy လုပ်နေဆဲ
- 🔴 **Failed** - Error ဖြစ်နေတယ်
- ⚪ **Suspended** - Stopped

## 💰 Pricing

### Free Tier (စတင်ရန်)
- ✅ 750 hours/month
- ✅ 512 MB RAM
- ✅ 1 GB disk
- ⚠️ Cold starts (slow wake-up)

### Starter Plan ($7/month)
- ✅ Unlimited hours
- ✅ No cold starts
- ✅ Better performance
- ✅ Recommended for production

## 🎯 Next Steps

1. ✅ **Deploy successful ဖြစ်ရင်:**
   - Characters ထည့်ပါ
   - Group မှာ test ကစားကြည့်ပါ
   - Friends တွေကို invite လုပ်ပါ

2. 📈 **Production ready ဖြစ်ချင်ရင်:**
   - Starter plan upgrade လုပ်ပါ
   - Persistent disk add လုပ်ပါ
   - Monitoring setup လုပ်ပါ

3. 🔧 **Customize ချင်ရင်:**
   - Code ကို modify လုပ်ပါ
   - GitHub push လုပ်ပါ
   - Render က auto-deploy လုပ်မယ်

## 📚 Additional Resources

- **Full Guide:** `DEPLOYMENT.md`
- **Project README:** `README.md`
- **Testing Guide:** `TESTING_GUIDE.md`
- **Security:** `SECURITY.md`

## 🆘 Need Help?

**Render API က error ပြရင်:**
```bash
# Check API key
echo "API Key: rnd_uAdpSqV7J9Fj4lZEKDQ6SXSaOXpJ"

# Test API connection
curl -H "Authorization: Bearer rnd_uAdpSqV7J9Fj4lZEKDQ6SXSaOXpJ" \
     https://api.render.com/v1/owners
```

**Script run လို့ မရရင်:**
```bash
# Make executable
chmod +x github_setup.sh
chmod +x deploy_to_render.py

# Install dependencies
pip3 install requests python-dotenv
```

---

## 🚀 Ready to Deploy?

```bash
# Run these commands:
./github_setup.sh
python3 deploy_to_render.py
```

Good luck! 🎉

Made with ❤️ in Myanmar 🇲🇲

