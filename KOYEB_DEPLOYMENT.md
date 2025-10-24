# 🚀 Koyeb Deployment Guide

## 📋 Prerequisites

1. ✅ [Koyeb Account](https://app.koyeb.com/auth/signup) (Free tier available)
2. ✅ GitHub repository with bot code
3. ✅ Telegram Bot Token
4. ✅ PostgreSQL Database URL
5. ✅ Google Gemini API Key

---

## 🎯 Step-by-Step Deployment

### **1️⃣ Create Koyeb Account**

1. သွားပါ: https://app.koyeb.com/auth/signup
2. GitHub account နဲ့ sign up လုပ်ပါ
3. Email verify လုပ်ပါ

---

### **2️⃣ Connect GitHub Repository**

1. Koyeb Dashboard မှာ **"Create Service"** နှိပ်ပါ
2. **"GitHub"** ရွေးပါ
3. Repository authorize လုပ်ပါ
4. **Repository** ရွေးပါ: `Wyattx3/mami`
5. **Branch** ရွေးပါ: `main`

---

### **3️⃣ Configure Deployment**

#### **Builder Settings:**
- **Builder**: `Dockerfile`
- **Dockerfile Path**: `Dockerfile` (root directory)
- **Build Context**: `/` (root)

#### **Instance Settings:**
- **Region**: ရွေးပါ (e.g., `Washington D.C. (us-east)`)
- **Instance Type**: `Free` (512MB RAM, 1 vCPU)
- **Scaling**: 
  - **Min**: `1`
  - **Max**: `1` (Important: Bot တစ်ခုပဲ run ရမယ်!)

#### **Port Settings:**
- **Port**: `8080` (Dockerfile က expose လုပ်ထားတဲ့ port)
- **Protocol**: `HTTP`
- **Health Check Path**: `/` (optional)

---

### **4️⃣ Environment Variables**

**"Environment Variables"** section မှာ ထည့်ပါ:

```bash
# Required Variables
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
DATABASE_URL=postgresql://user:password@host:port/database
GEMINI_API_KEY=your_gemini_api_key_here

# Webhook Configuration (အရေးကြီးဆုံး!)
WEBHOOK_URL=https://your-app-name.koyeb.app
WEBHOOK_PATH=/webhook
PORT=8080

# Optional Game Settings
MIN_PLAYERS=4
MAX_PLAYERS=20
ROUND_DURATION=60
```

#### **🔗 WEBHOOK_URL Setup:**

Koyeb က auto-generate လုပ်တဲ့ URL format:
```
https://[your-service-name]-[your-org-name].koyeb.app
```

**Example:**
```
https://mami-bot-wyattx3.koyeb.app
```

⚠️ **Important**: Service name သိမှ webhook URL ရပါမယ်။ ပထမ deploy လုပ်တဲ့အခါ:
1. Deploy without `WEBHOOK_URL` first (bot will run in polling mode temporarily)
2. Deployment success ဖြစ်ရင် Koyeb က URL ပေးမယ်
3. URL ရပြီးရင် `WEBHOOK_URL` ထည့်ပြီး redeploy လုပ်ပါ

---

### **5️⃣ Advanced Settings (Optional)**

#### **Health Checks:**
```yaml
HTTP GET /
Port: 8080
Interval: 60s
Timeout: 5s
Grace Period: 90s
```

#### **Auto Restart:**
- **Restart Policy**: `Always`
- **Max Restart Count**: `10`

---

### **6️⃣ Deploy!**

1. အပေါ်က settings တွေ ပြည့်စုံအောင် စစ်ပါ
2. **"Deploy"** button နှိပ်ပါ
3. Deployment logs ကြည့်ပါ:
   - Building Docker image...
   - Pushing to registry...
   - Starting container...
   - Application running!

---

## 🎯 Get Your Webhook URL

### **Method 1: From Koyeb Dashboard**

1. Service page မှာ **"Deployments"** tab သွားပါ
2. **"Public URL"** ကို copy လုပ်ပါ
   ```
   Example: https://mami-bot-wyattx3.koyeb.app
   ```

### **Method 2: From Service Settings**

1. Service Overview မှာ **"Domains"** section ကြည့်ပါ
2. Default domain ကို copy လုပ်ပါ

---

## 🔄 Update Webhook URL

### **After Getting URL:**

1. **Koyeb Dashboard** → **Service** → **Settings**
2. **Environment Variables** → **Edit**
3. Add/Update:
   ```bash
   7bb4fd57-efbe-41cc-8612-ebebbe9e9c5e.cname.koyeb.app=https://your-actual-url.koyeb.app
   ```
4. **Save** နှိပ်ပါ
5. Koyeb က auto redeploy လုပ်ပါမယ်

---

## 📊 Monitoring

### **View Logs:**

1. **Service Dashboard** → **"Logs"** tab
2. Real-time logs ကြည့်နိုင်ပါမယ်
3. အောက်ပါ messages တွေ ရှာပါ:
   ```
   ✅ Bot starting up...
   ✅ Database connection pool created
   ✅ Database initialized successfully
   ✅ Mode: WEBHOOK
   ✅ Starting webhook server on port 8080
   ✅ Webhook URL: https://your-url.koyeb.app/webhook
   ```

### **Check Health:**

```bash
curl https://your-app-name.koyeb.app/
# Should return: {"status": "ok", "bot": "running"}
```

---

## 🔧 Troubleshooting

### **Problem 1: "Event loop is closed" Error**

✅ **Fixed**: `db_manager.py` မှာ connection handling ပြင်ထားပြီး

### **Problem 2: "RuntimeError: To use start_webhook..."**

✅ **Fixed**: `requirements.txt` မှာ `python-telegram-bot[webhooks]==21.5` ထည့်ထားပြီး

### **Problem 3: Bot Running in Polling Mode**

**Check:**
```bash
# Logs မှာ ဒီလိုမြင်ရမယ်:
Mode: WEBHOOK ✅
Mode: POLLING ❌ (Wrong!)
```

**Fix:**
- `WEBHOOK_URL` environment variable ထည့်ထားလား စစ်ပါ
- Redeploy လုပ်ပါ

### **Problem 4: Port Binding Error**

**Error:**
```
OSError: [Errno 98] Address already in use
```

**Fix:**
- PORT environment variable က `8080` ဖြစ်ဖို့ သေချာပါစေ
- Dockerfile EXPOSE `8080` ဖြစ်ဖို့ စစ်ပါ

### **Problem 5: Webhook Not Receiving Updates**

**Check:**
1. WEBHOOK_URL မှန်ကန်လား:
   ```bash
   echo $WEBHOOK_URL
   # Should be: https://your-app.koyeb.app (NO /webhook!)
   ```

2. Telegram webhook status:
   ```bash
   curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo
   ```

**Fix:**
- Re-deploy bot (Bot က webhook ကို auto-register လုပ်ပါမယ်)

---

## 💰 Free Tier Limits

Koyeb Free Tier:
- ✅ **2 Services** (2 bots run နိုင်ပါတယ်)
- ✅ **512MB RAM** per service
- ✅ **1 vCPU** per service
- ✅ **2.5GB Build Storage**
- ✅ **No credit card required**
- ✅ **Always-on** (24/7)

---

## 🎯 Quick Commands

### **View Service Status:**
```bash
# Koyeb CLI (optional)
koyeb service list
koyeb service get <service-name>
```

### **Check Logs:**
```bash
koyeb service logs <service-name> --follow
```

### **Restart Service:**
```bash
koyeb service redeploy <service-name>
```

---

## 🔐 Security Best Practices

1. ✅ **Never commit secrets** to Git
2. ✅ **Use Environment Variables** for all sensitive data
3. ✅ **Enable Auto-Updates** (Koyeb auto-deploys on git push)
4. ✅ **Monitor Logs** regularly
5. ✅ **Use HTTPS** only (Koyeb provides free SSL)

---

## 📚 Additional Resources

- 📖 [Koyeb Documentation](https://www.koyeb.com/docs)
- 🐳 [Dockerfile Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- 🤖 [Telegram Bot API](https://core.telegram.org/bots/api)
- 🔗 [Webhook Guide](https://core.telegram.org/bots/webhooks)

---

## ✅ Deployment Checklist

- [ ] Koyeb account created
- [ ] GitHub repository connected
- [ ] Dockerfile present in root
- [ ] `requirements.txt` updated with `[webhooks]`
- [ ] Environment variables configured
- [ ] `TELEGRAM_BOT_TOKEN` added
- [ ] `DATABASE_URL` added
- [ ] `GEMINI_API_KEY` added
- [ ] `PORT=8080` set
- [ ] First deployment completed
- [ ] Webhook URL obtained
- [ ] `WEBHOOK_URL` environment variable added
- [ ] Redeployed with webhook URL
- [ ] Logs checked for "Mode: WEBHOOK"
- [ ] Bot tested in Telegram

---

## 🎉 Success Indicators

Logs မှာ ဒီလိုမြင်ရရင် အောင်မြင်ပါပြီ:

```
✅ Bot starting up...
✅ Database connection pool created
✅ Database initialized successfully
✅ Mode: WEBHOOK
✅ Starting webhook server on port 8080
✅ Webhook URL: https://your-app.koyeb.app/webhook
✅ Application started
```

Bot ကို Telegram မှာ test လုပ်ပါ:
```
/start
Help Button နှိပ်ပါ
Group ထဲ add လုပ်ပါ
/creategame 5 နဲ့ စမ်းပါ
```

---

## 🆘 Need Help?

- Koyeb Logs မြင်ရင် screenshot ပို့ပေးပါ
- Error messages တွေ copy လုပ်ပြီး ပို့ပေးပါ
- Bot behavior ကို describe လုပ်ပါ

Happy Deploying! 🚀🎮


