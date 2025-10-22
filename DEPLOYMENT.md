# Render Deployment Guide

Telegram Strategy Game Bot ကို Render platform မှာ deploy လုပ်ရန် အဆင့်ဆင့် လမ်းညွှန်ချက်

## Prerequisites (လိုအပ်ချက်များ)

1. **Render Account**
   - [Render.com](https://render.com) မှာ account ဖန်တီးပါ (Free tier available)

2. **GitHub Repository**
   - Project code ကို GitHub မှာ upload လုပ်ပါ
   - သို့မဟုတ် GitLab, Bitbucket သုံးနိုင်ပါတယ်

3. **API Keys**
   - Telegram Bot Token ([BotFather](https://t.me/botfather))
   - Google Gemini API Key ([Google AI Studio](https://makersuite.google.com/app/apikey))

## Deployment Steps (Deploy လုပ်ပုံ)

### Step 1: Prepare Repository

1. **Code ကို GitHub မှာ upload လုပ်ပါ:**

```bash
cd "/Users/apple/tele scy"
git init
git add .
git commit -m "Initial commit for Render deployment"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

2. **လိုအပ်တဲ့ files စစ်ဆေးပါ:**
   - ✅ `Procfile` (worker: python bot.py)
   - ✅ `render.yaml` (configuration)
   - ✅ `requirements.txt` (dependencies)
   - ✅ `bot.py` (main application)

### Step 2: Create Render Service

1. **Render Dashboard သို့ သွားပါ:**
   - [Render Dashboard](https://dashboard.render.com/)

2. **New Web Service ဖန်တီးပါ:**
   - "New +" button ကို နှိပ်ပါ
   - "Background Worker" ကို ရွေးပါ

3. **Repository ချိတ်ဆက်ပါ:**
   - "Connect repository" ကို နှိပ်ပါ
   - သင့် GitHub repo ကို ရွေးပါ
   - Render ကို GitHub access ပေးဖို့ authorize လုပ်ပါ

### Step 3: Configure Service

**Basic Configuration:**

```yaml
Name: telegram-strategy-game-bot
Region: Singapore (သို့မဟုတ် အနီးဆုံး region)
Branch: main
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: python bot.py
```

**Instance Type:**
- Free tier ကို ရွေးပါ (စတင်ရန်)
- Production အတွက် Starter သို့မဟုတ် Standard ကို upgrade လုပ်ပါ

### Step 4: Add Environment Variables

"Environment" tab သို့ သွားပြီး အောက်ပါ variables တွေ ထည့်ပါ:

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here
LOBBY_SIZE=9
TEAM_SIZE=3
ROUND_TIME=60
```

**Important Notes:**
- Secret values တွေကို သေချာ စစ်ဆေးပါ
- Spaces တွေ မပါအောင် သတိပြုပါ
- Bot token နဲ့ API key တွေ မှန်ကန်မှု စစ်ဆေးပါ

### Step 5: Deploy

1. **"Create Web Service" button ကို နှိပ်ပါ**
2. Render က automatically build နှင့် deploy လုပ်မယ်
3. Logs ကို ကြည့်ပြီး deployment status စစ်ဆေးပါ

### Step 6: Verify Deployment

1. **Logs စစ်ဆေးပါ:**
   - "Logs" tab သို့ သွားပါ
   - "Bot starting up..." message ကို ရှာပါ
   - "Bot is ready and starting to poll for updates..." ပေါ်ရမယ်

2. **Bot စမ်းကြည့်ပါ:**
   - Telegram မှာ သင့် bot ကို ရှာပါ
   - `/start` command ပို့ပါ
   - Response ပြန်လာရင် success!

## Configuration Options (အပိုဆောင်း configuration များ)

### Auto-Deploy Setup

Repository မှာ code update လုပ်တိုင်း အလိုအလျောက် deploy လုပ်ဖို့:

1. Render Dashboard → Settings
2. "Auto-Deploy" ကို enable လုပ်ပါ
3. Branch: `main` ရွေးပါ

### Custom Domain (Optional)

သင့်ကိုယ်ပိုင် domain သုံးချင်ရင်:

1. Settings → Custom Domains
2. Domain name ထည့်ပါ
3. DNS records configure လုပ်ပါ

### Monitoring and Alerts

1. **Health Checks:**
   - Render က service health ကို automatic စစ်ဆေးပါမယ်
   - Bot crash ရင် auto-restart လုပ်ပါမယ်

2. **Email Notifications:**
   - Settings → Notifications
   - Deployment နဲ့ health alert emails ရယူပါ

## Database Configuration

SQLite database သုံးထားတဲ့အတွက် persistent storage လိုပါတယ်:

### Option 1: Render Disk (Recommended)

1. **Add Persistent Disk:**
   - Settings → Disks
   - "Add Disk" ကို နှိပ်ပါ
   - Name: `game-database`
   - Mount Path: `/opt/render/project/src/database`
   - Size: 1GB (Free tier မှာ available)

2. **Update Database Path:**
   - `config.py` မှာ database path ကို `/opt/render/project/src/database/game.db` ပြောင်းပါ

### Option 2: External Database (Production)

PostgreSQL သို့မဟုတ် MySQL သုံးချင်ရင်:

1. Render PostgreSQL service ဖန်တီးပါ
2. Connection string ကို environment variable အနေနဲ့ ထည့်ပါ
3. Code ကို database adapter ပြောင်းပါ

## Character Database Setup

Bot deploy ပြီးရင် characters ထည့်ဖို့ မမေ့ပါနဲ့:

1. **Telegram မှာ bot ကို သွားပါ**
2. **`/addcharacter` command သုံးပါ**
3. **အနည်းဆုံး 12 characters ထည့်ပါ**
4. **Admin password:** `Wyatt#9810` သို့မဟုတ် `Yuyalay2000`

သို့မဟုတ် pre-populated database file upload လုပ်နိုင်ပါတယ်:

```bash
# Local မှာ characters ထည့်ပြီးရင်
scp database/game.db YOUR_RENDER_DISK_PATH/
```

## Troubleshooting (ပြဿနာဖြေရှင်းခြင်း)

### Bot မ start ဘူး

**Logs စစ်ဆေးပါ:**
```
Logs tab → ကြည့်ပါ
```

**အဖြစ်များတဲ့ errors:**

1. **"TELEGRAM_BOT_TOKEN must be set"**
   - Environment variables မှာ token ထည့်ထားခြင်း ရှိ/မရှိ စစ်ဆေးပါ
   - Token value မှာ space တွေ ပါ/မပါ စစ်ဆေးပါ

2. **"GEMINI_API_KEY must be set"**
   - Gemini API key ထည့်ထားခြင်း ရှိ/မရှိ စစ်ဆေးပါ
   - API key valid ဖြစ်/မဖြစ် စစ်ဆေးပါ

3. **"No module named 'telegram'"**
   - Build command မှန်ကန်မှု စစ်ဆေးပါ
   - `pip install -r requirements.txt` ရှိရမယ်
   - Manual redeploy လုပ်ပါ

4. **"Database permission denied"**
   - Persistent disk mount လုပ်ထားခြင်း ရှိ/မရှိ စစ်ဆေးပါ
   - Database path မှန်ကန်မှု စစ်ဆေးပါ

### Bot crash ဖြစ်နေတယ်

1. **Logs ကြည့်ပါ** - Error messages ရှာပါ
2. **Manual Restart** - "Manual Deploy" → "Clear build cache & deploy"
3. **Instance size** - Free tier က memory limit ရှိတယ်, upgrade လုပ်ပါ

### Bot slow လုပ်နေတယ်

1. **Free tier limitations:**
   - 750 hours/month free
   - Cold starts (15-30 seconds delay)
   - Upgrade to paid plan for always-on

2. **Optimize code:**
   - Database queries optimize လုပ်ပါ
   - AI requests ကို cache လုပ်ပါ

### Database data ပျောက်သွားတယ်

1. **Persistent disk မသုံးထားရင်:**
   - Deploy လုပ်တိုင်း data ပျောက်သွားမယ်
   - Persistent disk add လုပ်ပါ (Step above ကြည့်ပါ)

2. **Backup strategy:**
   - Regular database backups ယူပါ
   - External storage သုံးပါ (S3, Google Drive, etc.)

## Cost Estimation (ကုန်ကျစရိတ်)

### Free Tier (စတင်ရန် အကောင်းဆုံး)

- **Service:** Background Worker (Free)
- **Hours:** 750 hours/month
- **Disk:** 1GB persistent disk (Free)
- **Limitations:**
  - Cold starts (bot idle ဖြစ်ရင် restart slow)
  - 750 hours limit (≈31 days)
  - Shared resources

### Starter Plan ($7/month)

- **Benefits:**
  - No cold starts (always-on)
  - Better performance
  - Unlimited hours
  - 512 MB RAM
  - Recommended for production

### Standard Plan ($25/month)

- **Benefits:**
  - High performance
  - 2 GB RAM
  - Priority support
  - Recommended for popular bots

## Best Practices (အကောင်းဆုံး လုပ်ဆောင်ချက်များ)

1. **Version Control:**
   - Git tags သုံးပြီး versions track လုပ်ပါ
   - `git tag -a v1.0.0 -m "Initial release"`

2. **Environment Variables:**
   - Secrets ကို code မှာ မထည့်ပါနဲ့
   - Environment variables သုံးပါ

3. **Error Handling:**
   - Proper error logging implement လုပ်ပါ
   - Try-catch blocks သုံးပါ

4. **Monitoring:**
   - Log levels သုံးပါ (INFO, WARNING, ERROR)
   - Important events ကို log လုပ်ပါ

5. **Database Backups:**
   - Weekly backups schedule လုပ်ပါ
   - Backup script ရေးပါ

6. **Testing:**
   - Local မှာ test ပြီးမှ deploy လုပ်ပါ
   - Staging environment သုံးပါ

## Alternative Deployment Options

### 1. Railway.app
- Similar to Render
- Free tier available
- Easy deployment

### 2. Heroku
- Popular platform
- Good documentation
- Limited free tier (credit card required)

### 3. DigitalOcean App Platform
- $5/month minimum
- Good performance
- More control

### 4. AWS Elastic Beanstalk
- Scalable
- AWS ecosystem
- More complex setup

### 5. VPS (Recommended for full control)
- DigitalOcean Droplet: $6/month
- Vultr: $6/month
- Linode: $5/month
- Full control, requires more setup

## Support and Resources

### Render Documentation
- [Render Docs](https://render.com/docs)
- [Background Workers](https://render.com/docs/background-workers)
- [Environment Variables](https://render.com/docs/environment-variables)

### Community
- [Render Community Forum](https://community.render.com/)
- [Discord](https://render.com/discord)

### Project Documentation
- `README.md` - Project overview
- `TESTING_GUIDE.md` - Testing instructions
- `SECURITY.md` - Security guidelines

## Conclusion

Render မှာ deploy လုပ်ဖို့ အလွယ်တကူ ဖြစ်ပါတယ်။ Free tier က testing နဲ့ small projects အတွက် အလုံလောက်ပါတယ်။ Production အတွက် paid plan ကို upgrade လုပ်ဖို့ အကြံပြုပါတယ်။

Happy deploying! 🚀

---

**Questions or Issues?**
- Check logs first
- Review this guide
- Contact support

Made with ❤️ in Myanmar 🇲🇲

