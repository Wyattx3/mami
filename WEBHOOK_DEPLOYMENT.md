# 🚀 Webhook Deployment Guide

Bot က အခု **Webhook Mode** ကို support လုပ်ပါပြီ! Production deployment အတွက် webhook mode က အကောင်းဆုံးပါ။

## 🎯 Webhook Mode ရဲ့ အားသာချက်များ

✅ **Multiple Instances** - Horizontal scaling လုပ်နိုင်တယ်  
✅ **Instant Updates** - Telegram က directly updates ပို့ပေးတယ်  
✅ **More Efficient** - Polling မလိုဘူး  
✅ **Production Ready** - Enterprise-grade deployment  
✅ **Cost Effective** - Less resource usage

---

## 📋 Prerequisites

1. **Choreo Account** - https://console.choreo.dev
2. **GitHub Repository** - Code ကို push ထားရမယ်
3. **Neon PostgreSQL** - Database setup ပြီးထားရမယ်
4. **Bot Token** - @BotFather ကနေ ရယူထားရမယ်

---

## 🔧 Local Testing (Polling Mode)

Local development မှာ polling mode သုံးနိုင်ပါတယ်:

```bash
# Activate virtual environment
source venv/bin/activate

# Don't set WEBHOOK_URL - bot will auto-use polling mode
python bot.py
```

Bot က `WEBHOOK_URL` environment variable မရှိရင် automatically polling mode သုံးပါမယ်။

---

## 🌐 Choreo Deployment (Webhook Mode)

### Step 1: Push Code to GitHub

```bash
git add .
git commit -m "Enable webhook mode for production"
git push origin main
```

### Step 2: Create Component in Choreo

1. Go to https://console.choreo.dev
2. Click **+ Create** → **Service** → **Service**
3. **GitHub Repository**: Select your repo
4. **Branch**: `main`
5. **Buildpack**: Python
6. **Dockerfile Path**: `Dockerfile`
7. **Port**: `8080`

### Step 3: Configure Environment Variables

Go to **DevOps** → **Configs & Secrets** → **+ Add** ထည့်ပါ:

```bash
# Required Variables
TELEGRAM_BOT_TOKEN=8265058299:AAE0LjObVHgPSaXwGAdX_v1M_SNzN-LNlYA
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://neondb_owner:password@host/neondb

# Webhook Configuration (Important!)
WEBHOOK_URL=https://your-component-url.choreoapis.dev
WEBHOOK_PATH=/webhook
PORT=8080

# Game Configuration
LOBBY_SIZE=9
TEAM_SIZE=3
ROUND_TIME=60
```

⚠️ **Important**: `WEBHOOK_URL` ကို component ရဲ့ actual URL နဲ့ replace လုပ်ပါ!

### Step 4: Get Your Webhook URL

1. **DevOps** → **Deploy** → **Deploy** ကို နှိပ်ပါ
2. Build ပြီးတာနဲ့ **Invoke URL** ကို copy ကူးပါ
3. Example: `https://abc-123-def.choreoapis.dev`

### Step 5: Update WEBHOOK_URL Environment Variable

1. **DevOps** → **Configs & Secrets**
2. `WEBHOOK_URL` ကို edit လုပ်ပါ
3. Value: `https://abc-123-def.choreoapis.dev` (သင့် actual URL)
4. **Save** → **Redeploy**

### Step 6: Configure Scaling (Multiple Instances)

1. **DevOps** → **Configurations**
2. **Deployment Configuration**:
   ```yaml
   Replicas: 3          # Run 3 instances
   Min Replicas: 1
   Max Replicas: 5      # Auto-scale up to 5
   CPU: 0.5 cores
   Memory: 512Mi
   ```
3. **Save** → **Redeploy**

---

## ✅ Verify Deployment

### Check Logs

```bash
# Choreo Console → DevOps → Logs

# Look for these messages:
2025-10-23 17:27:16 - Bot starting up...
2025-10-23 17:27:16 - Mode: WEBHOOK
2025-10-23 17:27:20 - Starting webhook server on port 8080
2025-10-23 17:27:20 - Webhook URL: https://your-app.choreoapis.dev/webhook
2025-10-23 17:27:24 - Application started ✅
```

### Test Bot

1. Telegram မှာ bot ကို `/start` ပို့ကြည့်ပါ
2. `/help` command စမ်းကြည့်ပါ
3. Group မှာ `/newgame` စမ်းကြည့်ပါ

---

## 🔍 Troubleshooting

### Problem: "Webhook URL not set" Error

**Solution**: `WEBHOOK_URL` environment variable ကို Choreo မှာ ထည့်ပါ။

### Problem: Bot မ respond ဘူး

**Solution**: 
1. Choreo logs စစ်ပါ
2. `WEBHOOK_URL` က component URL နဲ့ match ဖြစ်ရမယ်
3. Port `8080` ကို expose လုပ်ထားရမယ်

### Problem: Multiple Instance Conflicts

**Solution**: Webhook mode မှာ multiple instances အဆင်ပြေပါတယ်! Telegram က automatically load balance လုပ်ပေးပါမယ်။

---

## 📊 Performance Comparison

| Feature | Polling Mode | Webhook Mode |
|---------|-------------|--------------|
| Multiple Instances | ❌ No | ✅ Yes |
| Response Time | ~1-5 seconds | < 100ms |
| Resource Usage | High (continuous polling) | Low (event-driven) |
| Scalability | Limited | Excellent |
| Production Ready | ⚠️ Not recommended | ✅ Recommended |

---

## 🔄 Switching Between Modes

### Local Development (Polling)
```bash
# Don't set WEBHOOK_URL in .env
python bot.py  # Auto-uses polling
```

### Production (Webhook)
```bash
# Set WEBHOOK_URL in Choreo environment variables
WEBHOOK_URL=https://your-app.choreoapis.dev
# Bot auto-detects and uses webhook mode
```

---

## 🎉 Summary

1. ✅ Code က webhook mode support ပါပြီ
2. ✅ Local မှာ polling mode သုံးလို့ရတယ်
3. ✅ Choreo မှာ webhook mode သုံးပြီး multiple instances run နိုင်တယ်
4. ✅ Auto-detection - `WEBHOOK_URL` ရှိလား မရှိလား စစ်ပြီး mode ရွေးတယ်

---

## 📝 Environment Variables Summary

```bash
# Required (All Modes)
TELEGRAM_BOT_TOKEN=your_bot_token
GEMINI_API_KEY=your_gemini_key
DATABASE_URL=postgresql://...

# Optional - Webhook Mode Only
WEBHOOK_URL=https://your-app.choreoapis.dev  # If set, uses webhook
WEBHOOK_PATH=/webhook                         # Default: /webhook
PORT=8080                                     # Default: 8080

# Game Config
LOBBY_SIZE=9
TEAM_SIZE=3
ROUND_TIME=60
```

---

**Ready to Deploy? Follow the steps above! 🚀**

For support: Contact @cchrist3lle

