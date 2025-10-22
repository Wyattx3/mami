# 🎮 Game Testing Guide

## ✅ Setup Complete!

### 📊 What's Ready:
- ✅ **12 Mock Characters** added to database
- ✅ **Testing Mode** configured (LOBBY_SIZE=1)
- ✅ **Bot** ready to run

---

## 🎯 Testing Mode Configuration

**Current Settings:**
- `LOBBY_SIZE = 1` (Only YOU need to join!)
- `TEAM_SIZE = 1` (1 player per team)
- `ROUND_TIME = 20` seconds (Faster testing)

---

## 📝 How to Test the Game

### Step 1: Start the Bot
```bash
cd "/Users/apple/tele scy"
source venv/bin/activate
python bot.py
```

### Step 2: Test in Telegram

#### **Private Chat Testing:**
1. Open your bot in Telegram
2. Send `/start`
3. You'll see: "Add to Group" and "Help" buttons ✅

#### **Group Chat Testing:**
1. Create a test group in Telegram
2. Add your bot to the group
3. Send `/start` in the group
4. Click "New Game" button
5. Click "Join" button
6. **Game will start immediately** (only 1 player needed!)

### Step 3: Play the Game

**Game Flow (Solo Testing):**
1. ✅ You join the lobby
2. ✅ Teams formed (3 teams with 1 player each - YOU)
3. ✅ Round 1 starts - You vote for ဘုရင် role
4. ✅ Round 2-5 continue automatically
5. ✅ Scoring happens
6. ✅ Winner announced

**⚠️ Note:** In testing mode, the other 2 teams will automatically get random character assignments since there's only 1 real player (you).

---

## 🔧 Switch Back to Normal Mode

When ready for real gameplay with 9 players:

**Edit `.env` file:**
```bash
LOBBY_SIZE=9
TEAM_SIZE=3
ROUND_TIME=60
```

Then restart the bot.

---

## 📋 Mock Characters Added

1. **Aung Aung** - ENTJ + Leo (Great Leader)
2. **Kyaw Kyaw** - ESTP + Aries (Brave Warrior)
3. **Zaw Zaw** - INTJ + Aquarius (Wise Advisor)
4. **Hla Hla** - ESTJ + Capricorn (Business-minded)
5. **Mya Mya** - ENFJ + Libra (Diplomatic)
6. **Thiha** - ISTP + Scorpio (Practical)
7. **Su Su** - INFJ + Pisces (Empathetic)
8. **Ko Ko** - ENTP + Gemini (Creative)
9. **Nwe Nwe** - ISTJ + Virgo (Systematic)
10. **Win Win** - ESFJ + Cancer (Caring)
11. **Phyu Phyu** - INFP + Taurus (Artistic)
12. **Lu Min Thant** - (Previously added)

---

## 🎯 Testing Checklist

- [ ] Bot starts without errors
- [ ] Private chat shows correct buttons
- [ ] Group chat shows "New Game" button
- [ ] Can join lobby
- [ ] Game starts with 1 player
- [ ] Voting works (20 seconds per round)
- [ ] All 5 rounds complete
- [ ] Scoring system works
- [ ] Results show correctly with explanations
- [ ] "Details" button shows score breakdown

---

## 🐛 If Issues Occur

**Check bot logs:**
```bash
tail -f bot_output.log
```

**Restart bot:**
```bash
pkill -f "python.*bot.py"
python bot.py > bot_output.log 2>&1 &
```

---

## 🎉 Ready to Test!

Your game is ready for solo testing. Have fun! 🚀

