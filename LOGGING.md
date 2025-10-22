# Debug Logging Documentation

## Overview

Comprehensive debug logging ကို code files အားလုံးမှာ ထည့်သွင်းပြီးပါပြီ။ သင့် application ရဲ့ လုပ်ဆောင်ချက် တိုင်းကို track လုပ်နိုင်ပါမယ်။

## Logging Levels

ဒီ project မှာ အောက်ပါ logging levels များကို သုံးထားပါတယ်:

### 1. **DEBUG**
- Detailed information for debugging
- Function calls, parameter values
- Internal state changes

### 2. **INFO**
- Important events and milestones
- User actions
- System state changes
- Successful operations

### 3. **WARNING**
- Unexpected situations (non-critical)
- Validation failures
- Fallback behaviors

### 4. **ERROR**
- Error conditions
- Exceptions
- Failed operations

## Logging by Module

### 1. Main Bot (`bot.py`)

**Command Handlers:**
- `/start` - User ID နှင့် username log လုပ်သည်
- `/help` - User ID log လုပ်သည်
- `/stats` - User ID log လုပ်သည်
- `/newgame` - User ID, username, character count log လုပ်သည်
- `/addcharacter` - Character addition process အဆင့်တိုင်း log လုပ်သည်

**Character Addition Flow:**
```
INFO: User started /addcharacter
DEBUG: User entered character name: [name]
WARNING: Invalid character name (non-English): [name]
DEBUG: User selected MBTI: [mbti]
DEBUG: User selected zodiac: [zodiac]
DEBUG: User entered admin password
WARNING: User entered incorrect admin password
INFO: User successfully added character: [name] (ID: [id])
ERROR: Error adding character: [error]
```

**Lobby Operations:**
```
DEBUG: Lobby callback: [action] from user [id]
```

**Startup:**
```
INFO: ===================================...
INFO: Bot starting up...
INFO: Database initialized
INFO: Bot is ready and starting to poll for updates...
```

### 2. Database Manager (`database/db_manager.py`)

**Database Initialization:**
```
INFO: Initializing database...
INFO: Database initialized successfully
```

**Character Operations:**
```
DEBUG: Adding character: [name] (MBTI: [mbti], Zodiac: [zodiac])
INFO: Character added successfully: [name] (ID: [id])
DEBUG: Fetching [n] random characters
DEBUG: Retrieved [n] random characters
```

**Lobby Operations:**
```
DEBUG: Adding player to lobby: [username] (ID: [user_id])
INFO: Player added to lobby: [username]
WARNING: Player already in lobby: [username]
DEBUG: Removing player from lobby: User ID [user_id]
INFO: Player removed from lobby: User ID [user_id]
WARNING: Player not in lobby: User ID [user_id]
INFO: Clearing lobby queue
```

**Game Operations:**
```
INFO: Creating new game...
INFO: Game created successfully - ID: [game_id]
DEBUG: Updating game [game_id] status to: [status]
INFO: Game [game_id] status updated to: [status]
DEBUG: Adding [n] players to game [game_id]
INFO: Added [n] players to game [game_id]
```

**Round Operations:**
```
DEBUG: Saving round selection - Game: [id], Round: [n], Team: [n], Character: [id]
INFO: Round selection saved - Game: [id], Round: [n], Team: [n]
DEBUG: Saving round score - Game: [id], Round: [n], Team: [n], Score: [score]
INFO: Round score saved - Game: [id], Round: [n], Team: [n], Score: [score]
```

### 3. Game Handler (`handlers/game_handler.py`)

**Game Flow:**
```
INFO: Starting new game - Chat: [chat_id], Message: [message_id]
DEBUG: Retrieved [n] players from lobby
WARNING: Not enough players to start game: [n]/[required]
INFO: Game created with ID: [game_id]
INFO: Teams formed - [n] teams created
INFO: Starting rounds for game [game_id]
ERROR: Game [game_id] not found in active games
```

**Round Management:**
```
INFO: Game [id] - Starting round [n]/[total]
DEBUG: Game [id] - Running round [n]
ERROR: Not enough characters in database: [n]/[required]
DEBUG: Game [id] - Team [n] - Sending voting for round [n]
DEBUG: Game [id] - Round [n] - Waiting [seconds] seconds for votes
DEBUG: Game [id] - Round [n] - Finalizing votes
```

**Game Completion:**
```
INFO: Game [id] - Finishing game and calculating results
DEBUG: Game [id] - Scoring completed
INFO: Game [id] - Winner determined: Team [n]
INFO: Game [id] - Game completed and cleaned up
```

### 4. Voting Handler (`handlers/voting_handler.py`)

**Voting Initialization:**
```
DEBUG: Initializing voting for game [game_id]
DEBUG: Initializing voting for game [game_id], round [round_number]
```

**Voting Process:**
```
INFO: Sending voting to team [team_id] - Game: [id], Round: [n]
DEBUG: Voting message sent to user [user_id]
ERROR: Error sending vote to user [user_id]: [error]
```

**Vote Recording:**
```
WARNING: Invalid vote callback data: [data]
INFO: Vote recorded - Game: [id], Round: [n], Team: [n], User: [id], Character: [id]
ERROR: Error updating vote message: [error]
```

**Vote Finalization:**
```
INFO: Finalizing voting - Game: [id], Round: [n]
DEBUG: Team [n] selection: Character [id] (Votes: {votes})
DEBUG: Clearing votes for game [game_id]
```

### 5. Lobby Handler (`handlers/lobby_handler.py`)

**Join Operations:**
```
DEBUG: Player attempting to join lobby: [username] (ID: [user_id])
INFO: Player already in lobby: [username]
INFO: Player joined lobby: [username]
DEBUG: Lobby count: [count]/[size]
INFO: Lobby full! Starting game with [count] players
```

**Quit Operations:**
```
DEBUG: Player attempting to quit lobby: User ID [user_id]
INFO: Player not in lobby: User ID [user_id]
INFO: Player quit lobby: User ID [user_id]
```

### 6. AI Service (`services/ai_service.py`)

**Character Descriptions:**
```
DEBUG: Generating AI description for character: [name]
INFO: AI description generated for [name]: [length] chars
ERROR: AI Error generating description: [error]
WARNING: Using fallback description for [name]
```

**Character-Role Scoring:**
```
DEBUG: Scoring character-role match: [name] for [role]
INFO: AI scored [name] for [role]: [score]/10
ERROR: AI Scoring Error: [error]
WARNING: Using fallback score for [name]: [score]/10
```

### 7. Scoring Service (`services/scoring_service.py`)

**Game Scoring:**
```
INFO: Scoring game [game_id]
DEBUG: Game [game_id] has [n] round entries
DEBUG: Scoring team [team_id]
DEBUG: Team [n] - Round [n] - Score: [score]
INFO: Game [game_id] scoring completed
INFO: Team [n]: [score] points
INFO: Winner determined: Team [n] with [score] points
```

## Log Output Format

Logs က အောက်ပါ format နဲ့ display လုပ်ပါမယ်:

```
2025-10-21 12:30:45 - module_name - LEVEL - Message
```

Example:
```
2025-10-21 12:30:45 - database.db_manager - INFO - Character added successfully: John (ID: 1)
2025-10-21 12:30:46 - handlers.lobby_handler - INFO - Player joined lobby: john_doe
2025-10-21 12:30:50 - handlers.game_handler - INFO - Game created with ID: 1
```

## Viewing Logs

### Console Output

Bot ကို run လိုက်ရင် logs တွေ console မှာ real-time မြင်ရပါမယ်:

```bash
python bot.py
```

### File Logging (Optional)

File ထဲမှာ logs သိမ်းချင်ရင် `bot.py` မှာ file handler ထည့်ပါ:

```python
import logging

# Add file handler
file_handler = logging.FileHandler('bot.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))

# Get root logger and add handler
logging.getLogger().addHandler(file_handler)
```

### Filtering Logs by Module

Specific module ရဲ့ logs ကိုပဲ ကြည့်ချင်ရင်:

```bash
python bot.py 2>&1 | grep "handlers.game_handler"
```

### Filtering by Level

Error logs ကိုပဲ ကြည့်ချင်ရင်:

```bash
python bot.py 2>&1 | grep "ERROR"
```

## Debugging Scenarios

### 1. Game Creation Issues

Check logs for:
```
- "Not enough players to start game"
- "Not enough characters in database"
- "Game created with ID"
- "Teams formed"
```

### 2. Voting Problems

Check logs for:
```
- "Sending voting to team"
- "Vote recorded"
- "Invalid vote callback data"
- "Finalizing voting"
```

### 3. AI Integration Issues

Check logs for:
```
- "Generating AI description"
- "AI Error"
- "Using fallback"
- "AI scored"
```

### 4. Database Issues

Check logs for:
```
- "Database initialized"
- "Character added successfully"
- "Player added to lobby"
- "Round selection saved"
```

### 5. Admin Password Issues

Check logs for:
```
- "User entered admin password"
- "User entered incorrect admin password"
- "User successfully added character"
```

## Log Level Configuration

Production မှာ log level ကို ပြောင်းလိုရင် `bot.py` မှာ:

```python
# For production (less verbose)
logging.basicConfig(level=logging.INFO)

# For development (more detailed)
logging.basicConfig(level=logging.DEBUG)

# For minimal logging
logging.basicConfig(level=logging.WARNING)
```

## Performance Monitoring

Logs ကို သုံးပြီး performance monitor လုပ်နိုင်ပါတယ်:

- **Game Duration**: "Starting new game" မှ "Game completed" အထိ time
- **Round Duration**: Round start မှ finalization အထိ time
- **AI Response Time**: AI request မှ response အထိ time
- **Player Count**: Lobby joins/quits tracking

## Troubleshooting Guide

### Common Issues နှင့် Related Logs

| Issue | What to Check in Logs |
|-------|----------------------|
| Bot not starting | Startup logs, Database initialization |
| Game not starting | Lobby count, Player count, Character count |
| Voting not working | Vote callback logs, Voting message logs |
| AI not working | AI service logs, Error logs, Fallback logs |
| Wrong winner | Scoring logs, Team scores, Character-role match scores |
| Character not adding | Admin password logs, Database errors |

## Best Practices

1. **Regular Monitoring**: Production မှာ logs ကို regularly check လုပ်ပါ
2. **Log Rotation**: File logging သုံးရင် log rotation setup လုပ်ပါ
3. **Error Alerts**: ERROR level logs တွေကို monitor လုპ်ပြီး alert setup လုပ်ပါ
4. **Privacy**: User passwords, API keys များကို log မလုပ်ပါနဲ့
5. **Performance**: DEBUG level က production မှာ slow ဖြစ်နိုင်ပါတယ်

## Log Analysis Tools

Logs ကို analyze လုပ်ဖို့:

```bash
# Count errors
grep "ERROR" bot.log | wc -l

# Find slow operations
grep "Waiting.*seconds" bot.log

# Track user activity
grep "User.*used" bot.log

# Monitor game completion
grep "Game.*completed" bot.log
```

---

**Note:** All logging functionality က production-ready ဖြစ်ပြီး debugging နဲ့ monitoring အတွက် အဆင်သင့် ဖြစ်ပါပြီ! 🎯


