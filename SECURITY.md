# Security Information

## Admin Access

### Character Addition Protection

`/addcharacter` command ကို admin access only ဖြစ်အောင် protect လုပ်ထားပါတယ်။

**Admin Password:** `Wyatt#9810`

### How It Works

1. User က character information အားလုံး ပေးပြီးသောအခါ
2. System က admin password တောင်းပါမယ်
3. Correct password (`Wyatt#9810`) ထည့်မှသာ character ကို database ထဲ သိမ်းမယ်
4. Wrong password ဆိုရင် character ကို မသိမ်းပါ

### Changing Admin Password

Admin password ကို ပြောင်းလိုရင် `bot.py` file ထဲမှာ ပြောင်းနိုင်ပါတယ်:

```python
# Line 36 in bot.py
ADMIN_PASSWORD = "YourNewPassword"
```

**အကြံပြုချက်:** Password ကို strong password သုံးပါ (letters, numbers, special characters)

### Why Password Protection?

1. **Prevent Spam**: လူတိုင်း characters ထည့်လို့ မရပါ
2. **Data Quality**: Admin တစ်ယောက်တည်းက quality control လုပ်နိုင်ပါတယ်
3. **Database Integrity**: Duplicate or invalid characters မဝင်အောင် ကာကွယ်ပေးပါတယ်

### Security Best Practices

1. ✅ Admin password ကို လုံခြုံစွာ သိမ်းဆည်းပါ
2. ✅ Trusted persons တွေကိုပဲ password ပေးပါ
3. ✅ မကြာခဏ password ပြောင်းပါ (recommended)
4. ✅ `.env` file ကို git မှာ commit မလုပ်ပါနဲ့
5. ✅ Production မှာ password ကို ပိုခိုင်မာအောင် သုံးပါ

### Alternative Security Methods

လက်ရှိ implementation မှာ hardcoded password သုံးထားပါတယ်။ Production environment အတွက် အောက်ပါ methods တွေကို စဉ်းစားနိုင်ပါတယ်:

1. **Environment Variables**: `.env` file မှာ password သိမ်းပါ
2. **User ID Whitelist**: Admin user IDs တွေကို check လုပ်ပါ
3. **Database-based Admins**: Admin list ကို database မှာ သိမ်းပါ
4. **OAuth/Authentication**: External auth service သုံးပါ

### Current Implementation

```python
# bot.py
ADMIN_PASSWORD = "Wyatt#9810"

async def char_password_received(update, context):
    password = update.message.text.strip()
    
    if password != ADMIN_PASSWORD:
        # Reject and cancel
        await update.message.reply_text("Wrong password!")
        return ConversationHandler.END
    
    # Save character to database
    ...
```

---

## Database Security

- SQLite database: `database/game.db`
- Backups ယူဖို့ မမေ့ပါနဲ့
- Production မှာ proper database permissions သတ်မှတ်ပါ

## API Keys Security

- **Never commit** `.env` file to git
- `.gitignore` မှာ `.env` ပါတာ သေချာပါစေ
- API keys တွေကို rotate လုပ်ပါ (periodically)
- Rate limiting စဉ်းစားပါ

---

**Note:** This is a basic security implementation. For production use, consider more robust authentication mechanisms.

