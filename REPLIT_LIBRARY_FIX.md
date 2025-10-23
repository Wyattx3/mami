# 🔧 Replit Library Fix - ImportError

## ❌ Error You're Seeing:

```
ImportError: cannot import name 'AcceptedGiftTypes' from 'telegram'
```

---

## ✅ Quick Fix

### **Replit Shell မှာ အောက်ပါ commands များကို အစဉ်လိုက် run ပါ:**

```bash
# 1. Stop the bot first (Click Stop button)

# 2. Pull latest code
git pull origin main

# 3. Remove old Python libraries
rm -rf .pythonlibs

# 4. Clear pip cache
pip cache purge

# 5. Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# 6. Run the bot (Click Run button)
```

---

## 📋 Step-by-Step Instructions

### **1. Stop Bot**
- Click "Stop" button in Replit

### **2. Open Shell**
- Click "Shell" tab

### **3. Pull Latest Code:**
```bash
git pull origin main
```

Expected output:
```
Updating bb8dfba..7cbca3f
Fast-forward
 requirements.txt | 10 +++++-----
 1 file changed, 5 insertions(+), 5 deletions(-)
```

### **4. Remove Old Libraries:**
```bash
rm -rf .pythonlibs
```

### **5. Clear Cache:**
```bash
pip cache purge
```

### **6. Reinstall Dependencies:**
```bash
pip install --force-reinstall -r requirements.txt
```

This will take 1-2 minutes. You'll see:
```
Installing collected packages: ...
Successfully installed python-telegram-bot-21.5 ...
```

### **7. Verify Installation:**
```bash
pip show python-telegram-bot
```

Should show:
```
Name: python-telegram-bot
Version: 21.5
```

### **8. Run Bot:**
- Click "Run" button
- Wait for "Bot is ready and starting to poll..."

---

## 🔍 What Changed?

**Old requirements.txt:**
```txt
python-telegram-bot==22.5  ❌ Too new, incompatible
```

**New requirements.txt:**
```txt
python-telegram-bot==21.5  ✅ Stable, compatible
google-generativeai==0.8.3  ✅ Updated
aiosqlite==0.20.0  ✅ Updated
python-dotenv==1.0.1  ✅ Updated
flask==3.0.3  ✅ Updated
```

---

## 🎯 Alternative: Fresh Install

**If above doesn't work:**

```bash
# 1. Delete entire .pythonlibs folder
rm -rf .pythonlibs

# 2. Delete __pycache__ folders
find . -type d -name "__pycache__" -exec rm -r {} +

# 3. Restart Repl
# Click "Stop" → Wait 5 seconds → Click "Run"
```

Replit will automatically reinstall all dependencies.

---

## 🐛 Troubleshooting

### **Still Getting ImportError?**

**Check Python version:**
```bash
python3 --version
```

Should be Python 3.10 or higher.

**Check installed version:**
```bash
pip show python-telegram-bot | grep Version
```

Must be `21.5`

**Force reinstall specific package:**
```bash
pip uninstall python-telegram-bot -y
pip install python-telegram-bot==21.5 --no-cache-dir
```

---

### **"No module named telegram" Error?**

```bash
pip install python-telegram-bot==21.5
```

---

### **"Permission denied" Error?**

```bash
# Use --user flag
pip install --user -r requirements.txt
```

---

## ✅ Verification Checklist

After fix, verify:

- [ ] `git pull` successful
- [ ] Libraries removed: `.pythonlibs` deleted
- [ ] Dependencies reinstalled
- [ ] Bot starts without import errors
- [ ] Console shows: "Bot is ready..."
- [ ] `/start` command works in Telegram

---

## 📝 Common Replit Issues

### **Issue 1: Cached Old Version**
**Solution:** Delete `.pythonlibs` and restart

### **Issue 2: Partial Installation**
**Solution:** Use `--force-reinstall` flag

### **Issue 3: Wrong Python Version**
**Solution:** Check with `python3 --version`

### **Issue 4: Corrupted Cache**
**Solution:** Run `pip cache purge`

---

## 🚀 Complete Fresh Start

**If nothing works, nuclear option:**

```bash
# 1. Stop bot
# 2. In Shell:

# Delete all Python artifacts
rm -rf .pythonlibs
rm -rf __pycache__
find . -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete

# Pull latest
git pull origin main

# Clean install
pip cache purge
pip install -r requirements.txt

# Delete database (optional - loses data)
rm database/game.db

# 3. Click Run
```

---

## 📊 Expected Output

**After successful fix:**

```
✅ Database initialized successfully
🎮 Setting up handlers...
✅ All handlers registered successfully
🤖 Bot is ready and starting to poll...
```

**No errors like:**
```
❌ ImportError: cannot import name 'AcceptedGiftTypes'
❌ ModuleNotFoundError: No module named 'telegram'
```

---

## 💡 Why This Happened?

**Cause:**
- Version `22.5` of `python-telegram-bot` has breaking changes
- `AcceptedGiftTypes` is not in all versions
- Replit cached incompatible version

**Fix:**
- Downgraded to stable version `21.5`
- Cleared cache
- Clean reinstall

---

## 🎉 Success Indicators

**1. No Import Errors:**
```
✅ Bot starts without ImportError
```

**2. Bot Polls:**
```
✅ "starting to poll..." message appears
```

**3. Commands Work:**
```
✅ /start responds in Telegram
✅ /newgame creates lobby
```

**4. Correct Version:**
```bash
$ pip show python-telegram-bot
Version: 21.5 ✅
```

---

## 📞 Still Stuck?

**Quick Debug Command:**
```bash
# Run all checks
echo "=== Python Version ==="
python3 --version
echo "=== Telegram Bot Version ==="
pip show python-telegram-bot | grep Version
echo "=== Git Status ==="
git status
echo "=== Requirements ==="
cat requirements.txt
```

Copy the output and check:
- Python version ≥ 3.10
- telegram-bot version = 21.5
- requirements.txt updated

---

**Updated:** October 2025  
**Commit:** 7cbca3f  
**Fix:** python-telegram-bot version 21.5

