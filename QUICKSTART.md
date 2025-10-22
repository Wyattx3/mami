# Quick Start Guide

## 🚀 အမြန် စတင်နည်း

### 1. Setup လုပ်ရန်

```bash
# ပထမဆုံး setup script ကို run ပါ
chmod +x setup.sh
./setup.sh
```

### 2. API Keys ထည့်ရန်

`.env` file ကို edit လုပ်ပါ:

```bash
nano .env
```

အောက်ပါ keys တွေကို ထည့်ပါ:

```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
GEMINI_API_KEY=AIzaSyA-1234567890abcdefghijklmnop
```

**API Keys ရယူနည်း:**

- **Telegram Bot**: [@BotFather](https://t.me/botfather) မှာ `/newbot` ပို့ပါ
- **Gemini AI**: [Google AI Studio](https://makersuite.google.com/app/apikey) မှာ ဖန်တီးပါ

### 3. Bot ကို စတင်ရန်

```bash
# Virtual environment activate လုပ်ပါ
source venv/bin/activate

# Bot ကို run ပါ
python bot.py
```

### 4. Characters ထည့်ရန်

Bot က run နေပြီဆိုရင်:

1. Telegram မှာ သင့် bot ကို ရှာပါ
2. `/addcharacter` command ပို့ပါ
3. Character name ကို ရိုက်ပါ (English letters only)
4. MBTI type ကို button နဲ့ ရွေးပါ
5. Zodiac sign ကို button နဲ့ ရွေးပါ
6. AI က auto-generated description ပြပါမယ်
7. Admin password (`Wyatt#9810`) ကို ရိုက်ပါ
8. အနည်းဆုံး **12 characters** ထည့်ပါ

**အကြံပြုချက်:** 15-20 characters ထည့်ထားရင် game က ပိုကောင်းပါမယ်။

**Admin Password:** `Wyatt#9810` (security အတွက်)

### 5. Game စတင်ရန်

1. `/newgame` command ပို့ပါ
2. **Join Game** button ကို နှိပ်ပါ
3. Player 9 ယောက် ပြည့်တဲ့အခါ game အလိုအလျောက် စပါမယ်
4. ပျော်မွေ့ပါစေ! 🎉

---

## 📝 Commands အကျဉ်း

| Command | လုပ်ဆောင်ချက် |
|---------|---------------|
| `/start` | Welcome message |
| `/help` | အကူအညီ |
| `/newgame` | Game အသစ် |
| `/addcharacter` | Character ထည့်မယ် (Admin only, password required) |
| `/stats` | Statistics ကြည့်မယ် |
| `/cancel` | Current operation ကို cancel လုပ်မယ် |

---

## 🎮 Game Rules အကျဉ်း

1. **9 Players**, 3 Teams (3 players each)
2. **5 Rounds** of voting:
   - Round 1: ဘုရင် (Leader)
   - Round 2: စစ်သူကြီး (Warrior)
   - Round 3: အကြံပေး (Advisor)
   - Round 4: လယ်သမား (Farmer)
   - Round 5: ဘုန်းကြီး (Monk)
3. **60 seconds** per round
4. **AI scoring** based on MBTI & Zodiac
5. **Highest score wins!** 🏆

---

## ⚠️ Troubleshooting

### "Not enough characters" error
```bash
# Database မှာ characters စစ်ကြည့်ပါ
# Bot မှာ /stats command ပို့ပါ
# 12 characters အောက် ဆိုရင် characters ထပ်ထည့်ပါ
```

### Bot doesn't start
```bash
# API keys စစ်ကြည့်ပါ
cat .env

# Virtual environment activate ဖြစ်မဖြစ် စစ်ပါ
which python  # Should show venv/bin/python
```

### Bot crashes during game
```bash
# Logs ကြည့်ပါ
# Gemini API quota စစ်ပါ
# Database ကို reset လုပ်ပါ:
rm database/game.db
python bot.py
```

---

## 🎯 VPS Deployment (Quick)

```bash
# 1. Upload to VPS
scp -r "tele scy/" user@vps-ip:/home/user/

# 2. SSH into VPS
ssh user@vps-ip

# 3. Setup
cd tele\ scy/
./setup.sh

# 4. Configure .env
nano .env

# 5. Run with screen
screen -S bot
python bot.py
# Ctrl+A then D to detach

# 6. Check status
screen -r bot
```

---

## 📱 Testing with Multiple Accounts

Game ကို စမ်းသပ်ဖို့ **9 Telegram accounts** လိုပါမယ်။

**Options:**
1. မိတ်ဆွေများကို ဖိတ်ပါ (အကောင်းဆုံး)
2. Testing group ဖန်တီးပါ
3. Bot को Public ဖြစ်အောင် လုပ်ပါ

**Minimum Test:** 3 accounts နဲ့ voting logic ကို စမ်းနိုင်ပါတယ် (code မှာ LOBBY_SIZE ကို 3 သို့ ပြောင်းပါ)

---

## 💡 Tips

1. **Characters ပိုထည့်ပါ:** MBTI 16 types အားလုံးကို cover လုပ်ပါ
2. **Descriptions ရေးပါ:** Characters တွေကို မှတ်မိလွယ်အောင် ကောင်းကောင်း ဖော်ပြပါ
3. **API Limits:** Gemini free tier မှာ daily limits ရှိပါတယ်
4. **Backup Database:** `database/game.db` ကို မကြာခဏ backup လုပ်ပါ

---

## 🤝 Support

Questions? Issues?
- Check `README.md` for detailed documentation
- Check `sample_characters.md` for character examples
- Review logs for errors

---

Happy Gaming! 🎮🎉


