# 🎯 Code Quality & Best Practices Guide

ဒီ document က bot ရဲ့ code quality ကို မြှင့်တင်ထားတဲ့ features တွေနဲ့ best practices တွေကို ရှင်းပြထားပါတယ်။

---

## 📋 Table of Contents

1. [State Management System](#1-state-management-system)
2. [Error Handling & Validation](#2-error-handling--validation)
3. [Structured Logging](#3-structured-logging)
4. [Database Transactions](#4-database-transactions)
5. [Best Practices](#5-best-practices)
6. [Usage Examples](#6-usage-examples)

---

## 1. State Management System

### 📌 Overview

Bot သည် persistent state management system သုံးပြီး၊ database မှာ game နဲ့ user states တွေကို သိမ်းထားပါတယ်။ Bot restart ဖြစ်သွားရင်တောင် states တွေကို ဆက်လက် သိမ်းဆည်းနိုင်ပါတယ်။

### 🔧 Implementation

```python
from utils.state_manager import state_manager, GameState, UserState

# Set game state
await state_manager.set_game_state(
    chat_id=chat_id,
    state=GameState.ROUND_VOTING,
    metadata={'round': 3, 'players_voted': 5}
)

# Get game state
state_data = await state_manager.get_game_state(chat_id)
current_state = state_data['state']  # GameState enum
metadata = state_data['metadata']     # Dict with additional data

# Set user state
await state_manager.set_user_state(
    user_id=user_id,
    chat_id=chat_id,
    state=UserState.VOTING,
    metadata={'team': 1, 'has_voted': False}
)

# Clear states (after game ends)
await state_manager.clear_game_state(chat_id)
await state_manager.clear_user_states(chat_id)
```

### 📊 Available States

**Game States:**
- `IDLE` - No active game
- `LOBBY_OPEN` - Waiting for players
- `TEAMS_FORMING` - Creating teams
- `ROUND_VOTING` - Round in progress
- `ROUND_RESULTS` - Showing results
- `GAME_ENDED` - Game completed
- `ERROR` - Error state

**User States:**
- `MENU` - Main menu
- `IN_LOBBY` - Joined lobby
- `PLAYING` - In active game
- `VOTING` - Currently voting
- `WAITING` - Waiting for others

### ✅ Benefits

- ✅ **Persistent**: States survive bot restarts
- ✅ **Consistent**: Database-backed state management
- ✅ **Metadata Support**: Store additional contextual data
- ✅ **Clean API**: Easy to use enums and functions

---

## 2. Error Handling & Validation

### 📌 Overview

Comprehensive error handling system with defensive programming and input validation။

### 🔧 Custom Exceptions

```python
from utils.error_handler import BotError, ValidationError, DatabaseError, GameError

# Raise custom errors
raise ValidationError(
    message="Invalid bet amount",
    user_message="❌ လောင်းကြေးပမာဏ မမှန်ကန်ပါ။"
)

raise GameError(
    message="Cannot start game with insufficient players",
    user_message="❌ Player အရေအတွက် မလုံလောက်ပါ။"
)
```

### 🛡️ Input Validation

```python
from utils.error_handler import InputValidator

# Validate number input
is_valid, value, error_msg = InputValidator.validate_number(
    text=user_input,
    min_val=1,
    max_val=100
)

if not is_valid:
    await update.message.reply_text(error_msg)
    return

# Validate username
is_valid, error_msg = InputValidator.validate_username(username)

# Validate chat type
is_valid, error_msg = InputValidator.validate_chat_type(
    update,
    allowed_types=['group', 'supergroup']
)
```

### 🎯 Decorators for Error Handling

```python
from utils.error_handler import handle_command_errors, handle_callback_errors

# For command handlers
@handle_command_errors
async def my_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Your code here
    # Errors will be caught and reported automatically
    pass

# For callback handlers
@handle_callback_errors
async def my_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Your code here
    # Callback will be acknowledged automatically
    # Errors will be shown to user
    pass
```

### 🔒 Safe Operations

```python
from utils.error_handler import SafeOperations

# Safely send message (returns True/False)
success = await SafeOperations.safe_send_message(
    context, chat_id, "Hello!"
)

# Safely edit message
success = await SafeOperations.safe_edit_message(
    query, "Updated text"
)

# Safely answer callback
success = await SafeOperations.safe_answer_callback(
    query, "Done!"
)
```

### 📝 Error Reporting

```python
from utils.error_handler import ErrorReporter

# Report error to user
await ErrorReporter.report_error(
    update, context, error,
    user_message="စက်ပိုင်းဆိုင်ရာ ပြဿနာ ဖြစ်ပေါ်ခဲ့သည်။"
)

# Report validation error
await ErrorReporter.report_validation_error(
    update, context,
    "ကျေးဇူးပြု၍ ကိန်းဂဏန်း ထည့်ပါ။"
)
```

---

## 3. Structured Logging

### 📌 Overview

Professional logging system with:
- File rotation (10MB per file, 5 backups)
- Separate error log file
- Colored console output
- Structured log format

### 🔧 Basic Usage

```python
import logging

logger = logging.getLogger(__name__)

# Different log levels
logger.debug("Detailed debug information")
logger.info("✅ Operation completed successfully")
logger.warning("⚠️ Warning: Something might be wrong")
logger.error("❌ Error occurred", exc_info=True)
logger.critical("🚨 Critical system failure!")
```

### 📊 Game Event Logging

```python
from utils.logger_config import game_logger

# Log game events
game_logger.log_game_start(chat_id, player_count=9, lobby_size=9)
game_logger.log_round_complete(chat_id, round_number=3, votes_count=9)
game_logger.log_game_end(chat_id, winner_team="Team Alpha", duration_seconds=300)

# Log player actions
game_logger.log_player_action(
    user_id, chat_id,
    action="voted",
    details={'character_id': 123, 'round': 3}
)

# Log game errors
game_logger.log_error(
    error_type="invalid_vote",
    message="User voted after round ended",
    details={'user_id': user_id, 'round': 3}
)
```

### ⚡ Performance Logging

```python
from utils.logger_config import performance_logger
import time

# Log operation time
start = time.time()
# ... do operation ...
duration_ms = (time.time() - start) * 1000

performance_logger.log_operation_time(
    operation="team_formation",
    duration_ms=duration_ms,
    success=True
)

# Log database query performance
performance_logger.log_database_query(
    query_type="fetch_characters",
    duration_ms=25.5,
    rows_affected=40
)
```

### 📁 Log Files

```
logs/
├── telegram_bot.log          # All logs (rotated, 10MB max)
├── telegram_bot_errors.log   # Errors only (rotated, 10MB max)
└── ... (backup files)
```

### ⚙️ Configuration

```bash
# .env file
LOG_LEVEL=INFO              # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_DIR=logs                # Directory for log files
ENABLE_CONSOLE_LOGS=true    # Show logs in console
```

---

## 4. Database Transactions

### 📌 Overview

Atomic database operations with automatic rollback on errors။

### 🔧 Basic Transaction

```python
from database.transaction_manager import transaction_manager

# Simple transaction
async with transaction_manager.transaction():
    # All operations here are atomic
    await some_database_operation()
    await another_database_operation()
    # If any operation fails, all will rollback automatically
```

### 🎯 Critical Operations

```python
from database.transaction_manager import critical_ops

# Vote with validation (atomic)
success, message = await critical_ops.record_vote_with_validation(
    game_id=game_id,
    user_id=user_id,
    round_number=3,
    character_id=123
)

if success:
    await update.message.reply_text(message)
else:
    await update.message.reply_text(f"❌ {message}")

# Complete round atomically
success = await critical_ops.complete_round_atomically(
    game_id=game_id,
    round_number=3,
    team_scores={1: 10, 2: 5, 3: 8}  # Score increments for each team
)

# Cancel game with complete cleanup
success = await critical_ops.cancel_game_with_cleanup(
    game_id=game_id,
    chat_id=chat_id
)
```

### 🔒 Why Transactions?

**Without Transactions:**
```python
# ❌ Dangerous! Incomplete operations if crash occurs
await deduct_coins(user_id, 100)
# ... bot crashes here ...
await give_item(user_id, item_id)  # Never executes!
# User loses 100 coins but gets no item!
```

**With Transactions:**
```python
# ✅ Safe! Either both complete or both rollback
async with transaction_manager.transaction():
    await deduct_coins(user_id, 100)
    await give_item(user_id, item_id)
    # If either fails, both operations rollback
```

---

## 5. Best Practices

### ✅ DO's

#### State Management
```python
# ✅ Check state before operations
state_data = await state_manager.get_game_state(chat_id)
if state_data['state'] != GameState.ROUND_VOTING:
    await update.message.reply_text("ဂိမ်း voting အခန်းကန့်မှာ မရှိပါ။")
    return

# ✅ Update state after important operations
await state_manager.set_game_state(
    chat_id, GameState.ROUND_RESULTS
)
```

#### Error Handling
```python
# ✅ Validate input
is_valid, value, error_msg = InputValidator.validate_number(
    user_input, min_val=1, max_val=10
)
if not is_valid:
    await update.message.reply_text(error_msg)
    return

# ✅ Use decorators for handlers
@handle_command_errors
async def my_command(update, context):
    # Errors handled automatically
    pass

# ✅ Use custom exceptions
if player_count < MIN_PLAYERS:
    raise GameError(
        message=f"Insufficient players: {player_count}",
        user_message="❌ Player အရေအတွက် မလုံလောက်ပါ။"
    )
```

#### Logging
```python
# ✅ Log important events
logger.info(f"Game started: chat_id={chat_id}, players={count}")

# ✅ Log errors with context
logger.error(
    f"Failed to process vote: user_id={user_id}",
    exc_info=True,
    extra={'chat_id': chat_id, 'round': round_number}
)

# ✅ Use appropriate log levels
logger.debug("Detailed info for debugging")
logger.info("Normal operation")
logger.warning("Something unexpected")
logger.error("Operation failed")
logger.critical("System failure!")
```

#### Database Operations
```python
# ✅ Use transactions for critical operations
async with transaction_manager.transaction():
    await update_team_score(team_id, points)
    await record_achievement(user_id, achievement_id)

# ✅ Use prepared critical operations
success, msg = await critical_ops.record_vote_with_validation(...)
```

### ❌ DON'Ts

```python
# ❌ Don't ignore state
async def start_game(update, context):
    # Missing state check!
    await game_handler.start_game(chat_id)

# ❌ Don't trust user input
bet_amount = int(user_input)  # Crashes if not a number!

# ❌ Don't use bare except
try:
    await some_operation()
except:  # ❌ Catches everything, even KeyboardInterrupt!
    pass

# ❌ Don't use print() for logging
print("User joined")  # ❌ Won't be in log files!

# ❌ Don't perform critical operations without transactions
await deduct_coins(user_id, 100)
await add_item(user_id, item_id)  # If this fails, coins already deducted!
```

---

## 6. Usage Examples

### Example 1: Command Handler with Full Error Handling

```python
from utils.error_handler import handle_command_errors, InputValidator, ValidationError
from utils.state_manager import state_manager, GameState
from utils.logger_config import game_logger

@handle_command_errors
async def bet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /bet command with comprehensive error handling"""
    
    # Validate chat type
    is_valid, error_msg = InputValidator.validate_chat_type(
        update, allowed_types=['private']
    )
    if not is_valid:
        raise ValidationError(message=error_msg, user_message=error_msg)
    
    # Check game state
    state_data = await state_manager.get_game_state(update.effective_chat.id)
    if state_data['state'] != GameState.ROUND_VOTING:
        raise ValidationError(
            message="Bet attempted outside voting phase",
            user_message="❌ Voting အချိန်မဟုတ်ပါ။"
        )
    
    # Validate input
    if not context.args:
        raise ValidationError(
            message="No bet amount provided",
            user_message="❌ လောင်းကြေးပမာဏ ထည့်ပါ။\n\nExample: /bet 100"
        )
    
    is_valid, amount, error_msg = InputValidator.validate_number(
        context.args[0], min_val=10, max_val=1000
    )
    if not is_valid:
        raise ValidationError(message=error_msg, user_message=error_msg)
    
    # Process bet
    await process_bet(update.effective_user.id, amount)
    
    # Log action
    game_logger.log_player_action(
        update.effective_user.id,
        update.effective_chat.id,
        action="placed_bet",
        details={'amount': amount}
    )
    
    await update.message.reply_text(f"✅ လောင်းကြေး {amount} ထည့်ပြီးပါပြီ!")
```

### Example 2: Callback Handler with State Management

```python
from utils.error_handler import handle_callback_errors, GameError
from utils.state_manager import state_manager, UserState
from database.transaction_manager import critical_ops

@handle_callback_errors
async def vote_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle vote button callback"""
    query = update.callback_query
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    # Parse callback data
    _, character_id = query.data.split("_")
    character_id = int(character_id)
    
    # Check user state
    user_state_data = await state_manager.get_user_state(user_id, chat_id)
    if user_state_data['state'] != UserState.VOTING:
        raise GameError(
            message=f"User {user_id} attempted to vote in wrong state",
            user_message="❌ သင် vote ပေးနိုင်တဲ့ အချိန်မဟုတ်ပါ။"
        )
    
    # Record vote with transaction
    success, message = await critical_ops.record_vote_with_validation(
        game_id=user_state_data['metadata']['game_id'],
        user_id=user_id,
        round_number=user_state_data['metadata']['round'],
        character_id=character_id
    )
    
    if not success:
        raise GameError(message=f"Vote failed: {message}", user_message=message)
    
    # Update user state
    await state_manager.set_user_state(
        user_id, chat_id, UserState.WAITING,
        metadata={'has_voted': True}
    )
    
    await query.answer(message, show_alert=True)
```

### Example 3: Database Transaction for Game Completion

```python
from database.transaction_manager import transaction_manager, critical_ops
from utils.state_manager import state_manager, GameState
from utils.logger_config import game_logger, performance_logger
import time

async def complete_game(game_id: int, chat_id: int):
    """Complete game with all cleanup"""
    
    start_time = time.time()
    
    try:
        # Get final scores
        final_scores = await get_team_scores(game_id)
        winner_team = max(final_scores, key=final_scores.get)
        
        # Atomic game completion
        async with transaction_manager.transaction() as conn:
            # Mark game as completed
            await conn.execute(
                """
                UPDATE games 
                SET status = 'completed', 
                    winner_team = $1, 
                    ended_at = NOW()
                WHERE game_id = $2
                """,
                winner_team, game_id
            )
            
            # Award points to winner team members
            await conn.execute(
                """
                UPDATE user_stats 
                SET wins = wins + 1, 
                    total_points = total_points + 100
                WHERE user_id IN (
                    SELECT user_id FROM team_members 
                    WHERE game_id = $1 AND team_number = $2
                )
                """,
                game_id, winner_team
            )
            
            # Clear game states
            await state_manager.clear_game_state(chat_id)
            await state_manager.clear_user_states(chat_id)
        
        # Log completion
        duration_ms = (time.time() - start_time) * 1000
        game_logger.log_game_end(
            chat_id, winner_team=f"Team {winner_team}", 
            duration_seconds=int(duration_ms / 1000)
        )
        performance_logger.log_operation_time(
            "complete_game", duration_ms, success=True
        )
        
        return True, f"🏆 Team {winner_team} အနိုင်ရရှိပါသည်!"
        
    except Exception as e:
        game_logger.log_error(
            "game_completion_failed",
            str(e),
            details={'game_id': game_id, 'chat_id': chat_id}
        )
        return False, "ဂိမ်း ပြီးဆုံးရာတွင် အမှားဖြစ်ပေါ်ခဲ့သည်။"
```

---

## 🎓 Summary

### ✅ အောင်မြင်ချက်များ:

1. ✅ **State Management** - Database-backed persistent state system
2. ✅ **Error Handling** - Comprehensive validation and error reporting
3. ✅ **Structured Logging** - Professional logging with rotation
4. ✅ **Database Transactions** - Atomic operations with rollback
5. ✅ **Input Validation** - Defensive programming against bad input
6. ✅ **Documentation** - Clear code comments and guides

### 📈 Code Quality Improvements:

- **Before**: Errors crash the bot, no state persistence, basic logging
- **After**: Graceful error handling, persistent states, structured logging, atomic operations

### 🎯 Next Steps:

1. Review existing handlers and add error handling decorators
2. Replace direct database operations with transaction-based ones
3. Add state checks before critical operations
4. Improve logging in existing functions
5. Write unit tests for critical functions

---

## 📚 Additional Resources

- [State Manager API](utils/state_manager.py)
- [Error Handler API](utils/error_handler.py)
- [Logger Configuration](utils/logger_config.py)
- [Transaction Manager API](database/transaction_manager.py)

---

**Happy Coding! 🚀**

