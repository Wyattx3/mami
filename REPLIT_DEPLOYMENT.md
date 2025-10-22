# Replit Deployment Guide

Telegram Strategy Game Bot ကို Replit platform မှာ deploy လုပ်ရန် အဆင့်ဆင့် လမ်းညွှန်ချက်

## 🎯 Replit ရဲ့ အားသာချက်များ

- ✅ **အလွယ်ကူဆုံး setup** - Browser ထဲမှာ တိုက်ရိုက် code ရေးလို့ရ
- ✅ **Free tier ကောင်းတယ်** - Always free (Hacker plan မလိုဘူး)
- ✅ **Instant deployment** - Run button နှိပ်လိုက်ရုံ
- ✅ **Built-in editor** - IDE တပါတည်း
- ✅ **Auto-restart** - Crash ဖြစ်ရင် auto restart
- ⚠️ **Sleeping on free tier** - Idle ဖြစ်ရင် sleep သွားတယ် (keep_alive နဲ့ ဖြေရှင်းထား)

## Prerequisites (လိုအပ်ချက်များ)

1. **Replit Account**
   - [Replit.com](https://replit.com) မှာ account ဖန်တီးပါ (Free!)

2. **API Keys**
   - Telegram Bot Token ([BotFather](https://t.me/botfather))
   - Google Gemini API Key ([Google AI Studio](https://makersuite.google.com/app/apikey))

3. **GitHub Repository** (Optional)
   - Code ကို GitHub မှာ ထားရင် import လုပ်လို့ရတယ်
   - Manual upload လည်း လုပ်လို့ရတယ်

---

## 📋 Deployment Methods (ရွေးချယ်မှု 2 မျိုး)

### **Method 1: GitHub Import** (အကြံပြုတယ်) ⭐

GitHub repository ကနေ တိုက်ရိုက် import လုပ်ပါ

### **Method 2: Manual Upload**

Files တွေကို manual upload လုပ်ပါ

---

## 🚀 Method 1: GitHub Import (အလွယ်ကူဆုံး)

### **Step 1: Replit Account ဖန်တီးခြင်း**

1. **Replit website သို့ သွားပါ:**
   - [https://replit.com](https://replit.com) ဖွင့်ပါ

2. **Sign Up:**
   - **"Sign up"** button ကို နှိပ်ပါ
   - **"Continue with GitHub"** ကို ရွေးပါ (အလွယ်ဆုံး)
   - GitHub authorization လုပ်ပါ
   - သို့မဟုတ် email/Google နဲ့လည်း register လုပ်နိုင်ပါတယ်

3. **Profile Setup:**
   - Username ရွေးပါ
   - Free plan ကို ရွေးပါ (Hacker plan မလိုပါ)

---

### **Step 2: Import GitHub Repository**

1. **Dashboard သို့ သွားပါ:**
   - Login ပြီးရင် [https://replit.com/~](https://replit.com/~) မှာ ရောက်မယ်

2. **Create New Repl:**
   - **"+ Create Repl"** button ကို နှိပ်ပါ
   - **"Import from GitHub"** tab ကို ရွေးပါ

3. **Repository URL ထည့်ပါ:**
   ```
   https://github.com/Wyattx3/mami
   ```
   - "Import from GitHub" button ကို နှိပ်ပါ

4. **Configuration:**
   ```
   Language: Python
   Title: telegram-strategy-game (သို့မဟုတ် နာမည် သင်ကြိုက်သလို)
   ```

5. **Create Repl:**
   - **"Import from GitHub"** button ကို နှိပ်ပါ
   - Replit က automatic ဖန်တီးပေးမယ်
   - Project files တွေ download လုပ်မယ်

⏱️ **ကြာချိန်:** 1-2 minutes

---

### **Step 3: Environment Variables Setup** ⭐ (အရေးကြီးဆုံး!)

1. **Secrets Tab ဖွင့်ပါ:**
   - ဘယ်ဘက် sidebar မှာ **🔒 Secrets** (lock icon) ကို နှိပ်ပါ
   - သို့မဟုတ် **Tools → Secrets**

2. **API Keys ထည့်ပါ:**

#### **Secret 1: TELEGRAM_BOT_TOKEN**
```
Key: TELEGRAM_BOT_TOKEN
Value: 123456:ABCdefGHIjklMNOpqrsTUVwxyz
```

**ရယူပုံ:**
- Telegram မှာ [@BotFather](https://t.me/BotFather) ကို ရှာပါ
- `/newbot` ပို့ပါ
- Bot name နဲ့ username ပေးပါ (e.g., `MyGameBot`, `@mygame_bot`)
- Token ကို copy လုပ်ပါ

#### **Secret 2: GEMINI_API_KEY**
```
Key: GEMINI_API_KEY
Value: AIzaSyC... (သင့် Gemini key)
```

**ရယူပုံ:**
- [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey) သို့ သွားပါ
- Google account နဲ့ sign in လုပ်ပါ
- **"Create API Key"** နှိပ်ပါ
- API key ကို copy လုပ်ပါ

#### **Secret 3: REPLIT_DEPLOYMENT**
```
Key: REPLIT_DEPLOYMENT
Value: true
```
(Keep alive server ကို activate လုပ်ဖို့)

#### **Secret 4-6: Game Configuration** (Optional)
```
Key: LOBBY_SIZE
Value: 9

Key: TEAM_SIZE
Value: 3

Key: ROUND_TIME
Value: 60
```

**Secrets ထည့်ပုံ:**
1. "Key" box မှာ variable name ရိုက်ပါ
2. "Value" box မှာ value ရိုက်ပါ
3. **"Add new secret"** button ကို နှိပ်ပါ
4. အခြား secrets တွေအတွက် ထပ်လုပ်ပါ

⚠️ **Important:**
- Secrets တွေက case-sensitive ဖြစ်တယ်
- Space တွေ မပါအောင် သတိပြုပါ
- Quotes (`"`) မထည့်ပါနဲ့

---

### **Step 4: Run the Bot** 🎉

1. **Dependencies Install:**
   - Shell tab ဖွင့်ပါ (Console icon)
   - Command ရိုက်ပါ:
     ```bash
     pip install -r requirements.txt
     ```
   - သို့မဟုတ် automatic install လုပ်မယ်

2. **Run Button:**
   - Top မှာ ရှိတဲ့ **▶️ "Run"** button (စိမ်းရောင်) ကို နှိပ်ပါ
   - Bot start လုပ်မယ်

3. **Logs ကြည့်ပါ:**
   - Console မှာ မြင်ရမယ်:
     ```
     Bot starting up...
     Keep alive server started for Replit
     Database initialized
     Bot is ready and starting to poll for updates...
     ```

4. **Success Indicators:**
   - ✅ Output မှာ "Bot is ready" message
   - ✅ Webview မှာ "Bot is Running!" page ပေါ်တယ်
   - ✅ Console မှာ errors မရှိဘူး

---

### **Step 5: Test the Bot**

1. **Telegram မှာ bot ကို ရှာပါ:**
   - Bot username (`@your_bot_username`) ကို ရှာပါ
   - `/start` command ပို့ပါ

2. **Expected Response:**
   ```
   🎮 Telegram Strategy Game

   MBTI နှင့် Zodiac signs ကို အခြေခံထားတဲ့ 
   team-based strategy game ကြိုဆိုပါတယ်!
   ```

3. **Success!** ✅
   - Response ပြန်လာရင် deployment successful!

---

### **Step 6: Keep Alive Setup** (Free Tier အတွက်)

Replit free tier က idle ဖြစ်ရင် sleep သွားတယ်။ Keep alive ကို activate လုပ်ထားပါ:

#### **A. Internal Keep Alive** (ပါပြီးသား)
- `keep_alive.py` က Flask server run ထားတယ်
- Port 8080 မှာ HTTP server တစ်ခု run နေမယ်

#### **B. External Ping Service** (Optional, Recommended)

**UptimeRobot သုံးပါ:**

1. **UptimeRobot Account:**
   - [https://uptimerobot.com](https://uptimerobot.com) သို့ သွားပါ
   - Free account ဖန်တီးပါ

2. **Add New Monitor:**
   - Dashboard → **"+ Add New Monitor"**
   - Settings:
     ```
     Monitor Type: HTTP(s)
     Friendly Name: Telegram Bot
     URL: https://your-repl-name.your-username.repl.co
     Monitoring Interval: 5 minutes
     ```

3. **Save:**
   - **"Create Monitor"** နှိပ်ပါ
   - UptimeRobot က 5 minutes တိုင်း ping လုပ်မယ်
   - Bot က 24/7 awake ဖြစ်နေမယ်

**Alternative Services:**
- [Uptime Kuma](https://uptime.kuma.pet/) (Self-hosted)
- [Cron-job.org](https://cron-job.org/) (Free cron)
- [Freshping](https://www.freshworks.com/website-monitoring/) (Free monitoring)

---

### **Step 7: Database Setup**

SQLite database က automatic create ဖြစ်ပါမယ်:

1. **Database File:**
   - `database/game.db` က automatic ဖန်တီးမယ်
   - Replit က persistent storage ပေးတယ် (free tier မှာလည်း)

2. **Characters ထည့်ပါ:**
   - Bot ကို Telegram မှာ စတင်ပါ
   - `/addcharacter` command သုံးပါ
   - အောက်ပါ အဆင့်တွေ လိုက်နာပါ:

**Character Addition:**
```
/addcharacter

1. Name: Thor (English letters only)
2. MBTI: ENTJ (button ကနေ ရွေးပါ)
3. Zodiac: Aries (button ကနေ ရွေးပါ)
4. AI generates description automatically
5. Admin Password: Wyatt#9810
```

**အနည်းဆုံး 12 characters ထည့်ပါ:**
- Round 3 ခုအတွက် လုံလောက်မယ်
- Round 5 ခုအတွက် 20+ ထည့်ဖို့ recommend လုပ်ပါတယ်

---

## 🚀 Method 2: Manual Upload

GitHub မသုံးချင်ရင် manual upload လုပ်နိုင်ပါတယ်:

### **Step 1: Create New Repl**

1. **Replit Dashboard:**
   - **"+ Create Repl"** ကို နှိပ်ပါ

2. **Template ရွေးပါ:**
   - **"Python"** template ရွေးပါ
   - Title: `telegram-strategy-game`

3. **Create Repl:**
   - **"+ Create Repl"** နှိပ်ပါ

### **Step 2: Upload Files**

**Option A: Drag & Drop**
1. Files browser window ဖွင့်ပါ
2. Project folder ကို Replit file explorer ထဲ drag လုပ်ပါ

**Option B: Upload**
1. File explorer မှာ **⋮** (three dots) နှိပ်ပါ
2. **"Upload file"** သို့မဟုတ် **"Upload folder"** ရွေးပါ
3. Files တွေ ရွေးပြီး upload လုပ်ပါ

**Option C: Git Clone**
1. Shell tab ဖွင့်ပါ
2. Command run ပါ:
   ```bash
   git clone https://github.com/Wyattx3/mami.git .
   ```

### **Step 3: Continue from Method 1 Step 3**

Environment variables setup ကနေ ဆက်လုပ်ပါ (Method 1 Step 3 ကို ကြည့်ပါ)

---

## 🎮 Game Testing

Deploy ပြီးရင် game စမ်းကြည့်ပါ:

### **Solo Testing (1 Player):**

1. **Secrets မှာ LOBBY_SIZE ပြောင်းပါ:**
   ```
   LOBBY_SIZE=1
   ```

2. **Bot Restart:**
   - Stop button နှိပ်ပါ
   - Run button ထပ်နှိပ်ပါ

3. **Test Commands:**
   ```
   /start      → Welcome message
   /newgame    → Create lobby
   Join button → Start game immediately
   ```

### **Group Testing (9 Players):**

1. **LOBBY_SIZE ပြန်ပြောင်းပါ:**
   ```
   LOBBY_SIZE=9
   ```

2. **Group Chat ဖန်တီးပါ:**
   - Telegram မှာ group chat တစ်ခု create လုပ်ပါ
   - Bot ကို group မှာ admin အဖြစ် ထည့်ပါ

3. **Game Commands:**
   ```
   /start      → Welcome with "New Game" button
   /newgame    → Create lobby
   9 players join → Game auto starts
   ```

---

## 📊 Replit Dashboard Overview

### **Important Tabs:**

1. **Code Editor** 📝
   - Main coding area
   - File explorer ဘယ်ဘက်မှာ
   - Syntax highlighting

2. **Shell/Console** 💻
   - Terminal commands run ဖို့
   - Logs ကြည့်ဖို့
   - Debugging

3. **Secrets** 🔒
   - Environment variables
   - API keys
   - Sensitive data

4. **Files** 📁
   - Project structure
   - Upload/download files
   - File management

5. **Version Control** 🔄
   - Git integration
   - Commit history
   - Push/pull changes

---

## 🔧 Troubleshooting

### **Problem 1: Bot မ Start ဘူး**

**Check Logs:**
```
Console မှာ error messages ရှာပါ
```

**Common Errors:**

**A. "TELEGRAM_BOT_TOKEN must be set"**
```
Solution:
- Secrets tab ကို စစ်ဆေးပါ
- TELEGRAM_BOT_TOKEN ရှိမရှိ confirm လုပ်ပါ
- Value မှာ space မပါအောင် သေချာပါ
```

**B. "No module named 'telegram'"**
```
Solution:
Shell မှာ run ပါ:
pip install -r requirements.txt
```

**C. "Conflict: terminated by other getUpdates"**
```
Solution:
- Bot ကို နေရာ 2 ခုမှာ run မနေအောင် လုပ်ပါ
- Local bot ရှိရင် ပိတ်ပါ
- Replit မှာပဲ run ပါ
```

### **Problem 2: Bot Sleep သွားတယ် (Free Tier)**

**Solution:**
```
1. keep_alive.py က run နေမလား စစ်ဆေးပါ
2. REPLIT_DEPLOYMENT=true ထည့်ထားမလား စစ်ဆေးပါ
3. UptimeRobot setup လုပ်ပါ (Step 6 ကြည့်ပါ)
4. Hacker plan ($7/month) upgrade လုပ်ပါ - Always-on
```

### **Problem 3: Characters မထည့်လို့ရဘူး**

**Solution:**
```
1. Admin password မှန်မလား စစ်ဆေးပါ: Wyatt#9810
2. Bot ကို private chat မှာ message လုပ်ပါ
3. English letters only သုံးပါ character name မှာ
```

### **Problem 4: Database Errors**

**Solution:**
```
Shell မှာ:
1. rm -rf database/game.db
2. Stop bot
3. Run bot again (database recreate မယ်)
```

### **Problem 5: Slow Response**

**Solution:**
```
- Replit free tier က slow ဖြစ်နိုင်တယ်
- Hacker plan upgrade လုပ်ပါ
- Code optimization လုပ်ပါ
```

---

## 🔄 Updating Code

Code update လုပ်ချင်ရင်:

### **Method 1: Direct Edit** (ပိုလွယ်တယ်)
1. Replit editor မှာ file ကို ဖွင့်ပါ
2. Changes လုပ်ပါ
3. Auto-save ဖြစ်မယ်
4. Stop & Run again

### **Method 2: GitHub Sync**
1. GitHub repo မှာ changes push လုပ်ပါ
2. Replit Shell မှာ:
   ```bash
   git pull origin main
   ```
3. Bot restart လုပ်ပါ

---

## 💰 Replit Pricing

### **Free Tier** ⭐ (အကောင်းဆုံး စတင်ရန်)
- ✅ Unlimited projects
- ✅ Public repls
- ✅ 1 GB storage
- ✅ 500 MB RAM
- ⚠️ Sleeps after inactivity (keep_alive နဲ့ ဖြေရှင်းထား)
- ⚠️ Slower performance

### **Hacker Plan ($7/month)**
- ✅ Always-on repls (no sleeping!)
- ✅ Private repls
- ✅ 5 GB storage
- ✅ 2 GB RAM
- ✅ Better performance
- ✅ Custom domains
- **Recommended for production bots**

### **Pro Plan ($20/month)**
- ✅ All Hacker features
- ✅ More resources
- ✅ Priority support
- ✅ Advanced features

---

## 🎯 Best Practices

### **1. Environment Variables**
- API keys ကို code မှာ မထည့်ပါနဲ့
- Secrets tab မှာပဲ သိမ်းပါ

### **2. Error Handling**
- Logs ကို regularly ကြည့်ပါ
- Error messages ကို ဖတ်ပါ

### **3. Database Backups**
```bash
# Shell မှာ backup ယူပါ
cp database/game.db database/game_backup.db
```

### **4. Keep Bot Alive**
- UptimeRobot setup လုပ်ပါ
- သို့မဟုတ် Hacker plan upgrade လုပ်ပါ

### **5. Code Organization**
- Clean code ရေးပါ
- Comments ထည့်ပါ
- Version control သုံးပါ

---

## 🆚 Replit vs Other Platforms

| Feature | Replit | Render | Railway | Heroku |
|---------|--------|--------|---------|--------|
| **Setup** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Free Tier** | ✅ Good | ✅ Great | ✅ Limited | ❌ Paid only |
| **Always-On Free** | ❌ (need ping) | ✅ 750hrs | ❌ Limited | ❌ |
| **IDE Built-in** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Price** | $0-7/mo | $0-7/mo | $5+/mo | $7+/mo |
| **Best For** | Learning/Testing | Production | Startups | Enterprise |

**Recommendation:**
- 🎓 **Learning/Testing:** Replit (အလွယ်ကူဆုံး)
- 🚀 **Production (Free):** Render (always-on)
- 💼 **Production (Paid):** Replit Hacker ($7) သို့မဟုတ် Railway
- 🏢 **Enterprise:** AWS/Heroku

---

## 📚 Resources

### **Replit Documentation:**
- [Replit Docs](https://docs.replit.com/)
- [Python on Replit](https://docs.replit.com/programming-ide/getting-started-python)
- [Secrets & Environment Variables](https://docs.replit.com/programming-ide/workspace-features/secrets)

### **Community:**
- [Replit Community](https://replit.com/talk)
- [Discord](https://replit.com/discord)
- [Forum](https://ask.replit.com/)

### **Project Documentation:**
- `README.md` - Project overview
- `DEPLOYMENT.md` - Render deployment
- `TESTING_GUIDE.md` - Testing guide
- `SECURITY.md` - Security guidelines

---

## ✅ Deployment Checklist

- [ ] Replit account ဖန်တီးပြီး
- [ ] Repository import လုပ်ပြီး (သို့မဟုတ် files upload လုပ်ပြီး)
- [ ] Secrets ထည့်ပြီး (TELEGRAM_BOT_TOKEN, GEMINI_API_KEY)
- [ ] Dependencies install လုပ်ပြီး (`pip install -r requirements.txt`)
- [ ] Bot run ပြီး (▶️ Run button)
- [ ] Keep alive setup လုပ်ပြီး (REPLIT_DEPLOYMENT=true)
- [ ] UptimeRobot config လုပ်ပြီး (optional but recommended)
- [ ] Bot respond လုပ်ပြီး (`/start` test)
- [ ] Characters 12+ ထည့်ပြီး (`/addcharacter`)
- [ ] Game test လုပ်ပြီး (group မှာ `/newgame`)

---

## 🎉 Conclusion

Replit က Telegram bot deployment အတွက် အလွယ်ကူဆုံး platform တစ်ခုပါ။ Built-in IDE နဲ့ instant deployment က စတင်သူတွေအတွက် အကောင်းဆုံးပါ။

**Key Points:**
- ✅ Setup လွယ်ကူတယ်
- ✅ Free tier ကောင်းတယ်
- ✅ Browser ထဲမှာပဲ အားလုံး လုပ်လို့ရတယ်
- ⚠️ Production အတွက် Hacker plan ကို upgrade လုပ်ဖို့ recommend လုပ်ပါတယ်

Happy coding on Replit! 🚀💻

---

**Questions or Issues?**
- Check console logs first
- Review this guide
- Join Replit community
- Contact support

Made with ❤️ in Myanmar 🇲🇲

