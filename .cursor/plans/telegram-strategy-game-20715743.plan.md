<!-- 20715743-8d8e-4a6f-bbc7-6a8c1e5f2065 febd8802-b2f6-4e76-964e-14c93290eaf6 -->
# Random Theme System Implementation

## Overview

Implement a random theme selection system where each game randomly selects one of 30+ themes at lobby creation time. Themes include Kingdom builds, Family builds, Friend builds, Relationship builds, DC/Marvel, Football, and Myanmar Singers. Display themes with emojis for visual appeal.

## Implementation Steps

### 1. Create Theme Definition System

**File: `data/themes.py` (NEW)**

- Define all 30+ themes as a dictionary structure
- Each theme contains:
  - `id`: unique identifier
  - `name`: theme name (e.g., "Kingdom Build 2")
  - `emoji`: theme emoji (e.g., "👑" for Kingdom)
  - `roles`: list of 5 roles with MBTI suitability
- Theme categories:
  - Kingdom Build (1-6) - 👑 emoji
  - Family Build (1-4) - 👨‍👩‍👧‍👦 emoji
  - Friend Build (1-5) - 👥 emoji
  - Relationship Build (1-3) - 💕 emoji
  - DC Build (1-2) - 🦸 emoji
  - Marvel Build (1-2) - 🦸‍♂️ emoji
  - Football Build (1-3) - ⚽ emoji
  - Myanmar Singers Build (1-4) - 🎤 emoji

Example structure:

```python
THEMES = {
    'kingdom_2': {
        'id': 'kingdom_2',
        'name': 'Kingdom Build 2',
        'emoji': '👑',
        'category': 'Kingdom',
        'roles': {
            1: {'name': 'ဘုရင်', 'description': '...', 'suitable_mbti': [...]},
            2: {'name': 'ဘုရင်မ', 'description': '...', 'suitable_mbti': [...]},
            ...
        }
    },
    ...
}
```

### 2. Update Database Schema

**File: `database/db_manager.py`**

- Add columns to `games` table:
  - `theme_id TEXT` - stores selected theme ID
  - `theme_name TEXT` - stores theme display name
- Modify `init_database()` to add migration for new columns
- Add helper methods:
  - `set_game_theme(game_id, theme_id, theme_name)`
  - `get_game_theme(game_id)` returns theme info

### 3. Random Theme Selection on Lobby Creation

**File: `bot.py`**

- In `start_newgame_callback_handler()`:
  - Import themes from `data/themes.py`
  - Randomly select theme: `theme = random.choice(list(THEMES.values()))`
  - Store selected theme in context for later use
  - Update lobby message to display theme with emoji

**File: `handlers/lobby_handler.py`**

- Modify `create_lobby_message()` to accept theme parameter
- Display format: `🎮 **GAME LOBBY** - 👑 Kingdom Build 2`
- Show theme info in lobby message

### 4. Store Theme in Game Record

**File: `handlers/game_handler.py`**

- In `start_game()`:
  - Retrieve selected theme from context or pass as parameter
  - Store theme in games table when creating game record
  - Pass theme to all round handlers

### 5. Use Theme Roles Throughout Game

**File: `handlers/game_handler.py`**

- Modify round handling to use theme's roles instead of global ROLES
- Load theme roles from database on game start
- Pass theme roles to voting handler

**File: `handlers/voting_handler.py`**

- Accept theme roles as parameter
- Display theme-specific role names in voting messages
- Use theme roles for AI scoring

**File: `services/scoring_service.py`**

- Accept theme roles as parameter for scoring
- Use theme-specific MBTI suitability from theme definition

### 6. Update Message Displays

**File: `bot.py`**, **`handlers/game_handler.py`**, **`handlers/voting_handler.py`**

- Update all role name displays to use theme roles
- Show theme emoji in round announcements
- Format: "📋 Round 1 - 👑 ဘုရင်"

## Key Design Decisions

1. **Theme Selection Timing**: At lobby creation (before players join)
2. **Theme Availability**: All 30+ themes available with equal probability
3. **Theme Display**: Show emoji + name (e.g., "👑 Kingdom Build 2")
4. **Repetition**: Full random - can repeat themes across games
5. **Storage**: Store theme_id and theme_name in games table for retrieval

## Files to Create/Modify

### New Files

- `data/themes.py` - All theme definitions (~500 lines)

### Modified Files

- `database/db_manager.py` - Add theme columns and methods
- `bot.py` - Random theme selection on lobby creation
- `handlers/lobby_handler.py` - Display theme in lobby
- `handlers/game_handler.py` - Use theme roles throughout game
- `handlers/voting_handler.py` - Display theme-specific roles
- `services/scoring_service.py` - Use theme MBTI suitability
- `utils/constants.py` - Keep original ROLES as fallback

## Testing Considerations

- Test theme selection randomness
- Test all 30+ themes load correctly
- Test role names display properly
- Test MBTI matching with theme roles
- Test database theme storage/retrieval
- Test game flow with different themes

### To-dos

- [ ] Create project structure, requirements.txt, config files, and initialize environment
- [ ] Implement SQLite database with tables for characters, games, players, rounds, and lobby queue
- [ ] Create character model and /addcharacter command for manual character entry
- [ ] Implement lobby with join/quit buttons, real-time player list, and auto-start at 9 players
- [ ] Implement random team formation (3 teams x 3 players) and announcement system
- [ ] Create game state manager for 5 rounds with role progression and timer system
- [ ] Implement privacy-based voting with 4 character options, vote counting, and tie resolution
- [ ] Integrate Gemini AI for character descriptions and role-matching scoring with explanations
- [ ] Implement final scoring system, results display with details button, and winner determination
- [ ] Test all game flows with edge cases and prepare VPS deployment setup