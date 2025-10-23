# ⚡ Quick Webhook Setup - Choreo

## 🚀 5 မိနစ်အတွင်း Webhook Mode Setup လုပ်ပါ!

### Step 1: Redeploy from GitHub

1. Choreo Console ကို ဝင်ပါ: https://console.choreo.dev
2. Bot component ကို select လုပ်ပါ
3. **DevOps** → **Builds** → **Build from GitHub**
4. Wait for build to complete...

### Step 2: Get Webhook URL

Build ပြီးတာနဲ့:
1. **DevOps** → **Deploy** section ကို ကြည့်ပါ
2. **Invoke URL** ကို copy ကူးပါ
3. Example: `https://abc-123-def-456.choreoapis.dev`

### Step 3: Add Environment Variable

1. **DevOps** → **Configs & Secrets**
2. Click **+ Add**
3. Add this variable:
   ```
   Name: WEBHOOK_URL
   Value: https://abc-123-def-456.choreoapis.dev
   ```
   (သင့် actual Invoke URL ကို သုံးပါ)
4. Click **Save**

### Step 4: Configure Scaling

1. **DevOps** → **Configurations**
2. **Deployment Configuration**:
   ```yaml
   Replicas: 3
   Min Replicas: 1
   Max Replicas: 5
   ```
3. **Save**

### Step 5: Redeploy

1. **DevOps** → **Deploy**
2. Click **Deploy** button
3. Wait for deployment...

### Step 6: Verify

Check logs မှာ ဒီလို မြင်ရရင် အဆင်ပြေပါပြီ:
```
Bot starting up...
Mode: WEBHOOK ✅
Starting webhook server on port 8080
Webhook URL: https://your-app.choreoapis.dev/webhook
Application started
```

---

## ✅ Testing

1. Telegram ဖွင့်ပါ
2. Bot ကို `/start` ပို့ပါ
3. `/help` စမ်းကြည့်ပါ
4. Group chat မှာ `/newgame` စတင်ကြည့်ပါ

---

## 🎯 Complete Environment Variables List

Choreo မှာ ဒီ variables တွေ အကုန် ရှိမရှိ စစ်ပါ:

```bash
# Required
TELEGRAM_BOT_TOKEN=8265058299:AAE0LjObVHgPSaXwGAdX_v1M_SNzN-LNlYA
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=postgresql://neondb_owner:password@host/neondb

# Webhook (New!)
WEBHOOK_URL=https://your-component.choreoapis.dev
WEBHOOK_PATH=/webhook
PORT=8080

# Game Config
LOBBY_SIZE=9
TEAM_SIZE=3
ROUND_TIME=60
```

---

## 🔍 Troubleshooting

### Bot still in polling mode?
- ✅ Check `WEBHOOK_URL` environment variable ရှိရဲ့လား
- ✅ Redeploy လုပ်ပြီးပြီလား

### Bot not responding?
- ✅ Logs ကြည့်ပြီး errors ရှိလား စစ်ပါ
- ✅ `WEBHOOK_URL` က component URL နဲ့ match ဖြစ်ရမယ်

### Multiple instances conflict?
- ✅ Webhook mode မှာ multiple instances အဆင်ပြေတယ်!
- ✅ Polling mode ဆိုမှ conflict ဖြစ်တယ်

---

**ပြီးပြီ! Bot က အခု webhook mode နဲ့ production-ready ဖြစ်ပါပြီ! 🎉**

