# 🔄 Replit Update Guide

## Database Schema Fix - is_leader Column

---

## ❌ Error You're Seeing:

```
sqlite3.OperationalError: table game_players has no column named is_leader
```

---

## ✅ Quick Fix (Recommended)

### Option 1: Delete Database & Restart (Easiest)

**In Replit Shell:**
```bash
rm database/game.db
```

**Then click "Run" button**

The bot will automatically recreate the database with the correct schema.

**⚠️ Note:** This will delete all game history and characters. You'll need to re-add characters.

---

## 🔧 Alternative Fix (Keeps Data)

### Option 2: Run Migration Script

**In Replit Shell:**
```bash
python migrate_database.py
```

**Then click "Run" button**

This will add the `is_leader` column to your existing database without deleting data.

---

## 📥 Get Latest Code

### Pull from GitHub

**In Replit Shell:**
```bash
git pull origin main
```

This will update your code with the fix.

---

## 🎯 Step-by-Step Instructions

### Method 1: Fresh Start (Recommended for Replit)

1. **Stop the bot** (if running)
   - Click "Stop" button

2. **Open Shell in Replit**

3. **Delete old database:**
   ```bash
   rm database/game.db
   ```

4. **Pull latest code:**
   ```bash
   git pull origin main
   ```

5. **Run bot:**
   - Click "Run" button

6. **Verify:**
   - Check console for "Database initialized successfully"
   - Test `/start` command in Telegram

7. **Re-add characters:**
   ```
   /addcharacter
   ```

---

### Method 2: Migrate Existing Database

1. **Stop the bot**

2. **Open Shell in Replit**

3. **Pull latest code:**
   ```bash
   git pull origin main
   ```

4. **Run migration:**
   ```bash
   python migrate_database.py
   ```

5. **Verify migration:**
   - Should see "✅ Migration completed successfully!"

6. **Run bot:**
   - Click "Run" button

7. **Test game:**
   - Try `/newgame` in Telegram group

---

## 🔍 Verify Fix

After fixing, test these:

### 1. Bot Starts
```
Console should show:
✅ Database initialized successfully
✅ Bot is ready and starting to poll...
```

### 2. Game Works
```
In Telegram group:
/newgame → Should create lobby
Join with 9 players → Game should start
Teams should be announced with leaders
```

### 3. No Errors
```
Console should NOT show:
❌ table game_players has no column named is_leader
```

---

## 📊 What Changed?

### Database Schema Update

**Before:**
```sql
CREATE TABLE game_players (
    id INTEGER PRIMARY KEY,
    game_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    username TEXT,
    team_number INTEGER NOT NULL
);
```

**After:**
```sql
CREATE TABLE game_players (
    id INTEGER PRIMARY KEY,
    game_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    username TEXT,
    team_number INTEGER NOT NULL,
    is_leader INTEGER DEFAULT 0  -- NEW!
);
```

---

## 🐛 Troubleshooting

### Error Still Appears?

**1. Database not deleted:**
```bash
# Check if file exists
ls database/game.db

# Force delete
rm -f database/game.db
```

**2. Code not updated:**
```bash
# Pull again
git pull origin main

# Check database/db_manager.py has is_leader
grep "is_leader" database/db_manager.py
```

**3. Restart Repl:**
- Click "Stop"
- Wait 5 seconds
- Click "Run"

---

## 📝 Notes

### If Using Method 1 (Delete Database)

**You will lose:**
- ❌ All game history
- ❌ All characters in database
- ❌ All player records

**You will keep:**
- ✅ All code
- ✅ All configuration (Secrets)
- ✅ Bot token & API key

**You need to:**
- Re-add characters using `/addcharacter`
- Minimum 12 characters required

---

### If Using Method 2 (Migration)

**You will keep:**
- ✅ All characters
- ✅ All game history
- ✅ All configuration

**Migration adds:**
- ✅ `is_leader` column to existing records
- ✅ Default value: 0 (not leader)

---

## ✅ Verification Checklist

After applying fix:

- [ ] Bot starts without errors
- [ ] Console shows "Database initialized"
- [ ] `/start` works in private chat
- [ ] `/newgame` creates lobby in group
- [ ] 9 players can join
- [ ] Teams are announced
- [ ] Leaders are shown (👑 icon)
- [ ] Game proceeds without errors

---

## 🎉 Success!

Once you see this in console:
```
✅ Database initialized successfully
✅ Bot is ready and starting to poll...
```

And game works without errors, you're all set! 🚀

---

## 📞 Still Having Issues?

1. Check Repl console for full error message
2. Verify all Secrets are set correctly
3. Make sure database file was actually deleted
4. Try completely stopping and restarting Repl
5. Check that `git pull` actually updated files

---

**Updated:** October 2025  
**Commit:** 4029b78  
**Fix:** Database schema includes is_leader column


