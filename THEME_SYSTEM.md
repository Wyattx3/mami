# 🎮 Random Theme System - Fall Guys Style

## Overview
Bot တွင် အခု **29 မျိုးသော themes** ရှိပြီး၊ game တစ်ခု စတင်တိုင်း random theme တစ်ခု ရွေးချယ်သွားမှာ ဖြစ်ပါတယ်။ ဒါက Fall Guys game ရဲ့ "Random Room Selection" concept နဲ့ တူပါတယ်။

## Features

### 1. 29 Unique Themes
Bot တွင် အောက်ပါ categories များ ပါဝင်ပါတယ်:

#### Kingdom Build (6 themes) 👑
- Kingdom Build 1-6
- Roles: ဘုရင်, စစ်သူကြီး, အကြံပေး, လယ်သမား, ဘုန်းကြီး, etc.

#### Family Build (4 themes) 👨‍👩‍👧‍👦
- Family Build 1-4
- Roles: အဖိုး, အဖွား, အဖေ, အမေ, သား, သမီး, etc.

#### Friend Build (5 themes) 🤝
- Friend Build 1-5
- Roles: ဦးဆောင်တက်သူ, ဖာခေါင်း, နတ်သမီး, ငြင်းလေ့ရှိသူ, etc.

#### Relationship Build (3 themes) 💕
- Relationship Build 1-3
- Roles: ဒုတိယလူ, သစ္စာရှိသူ, Red Flag, Green Flag, etc.

#### DC Build (2 themes) 🦸
- DC Build 1-2
- Roles: Superman, Batman, Flash, Wonder Woman, Aquaman, etc.

#### Marvel Build (2 themes) 🦸
- Marvel Build 1-2
- Roles: Spider-Man, Iron Man, Captain America, Thor, Hulk, etc.

#### Football Player Build (3 themes) ⚽
- Football Player Build 1-3
- Roles: Messi, Ronaldo, Mbappe, Haaland, Yamal, etc.

#### Myanmar Singers Build (4 themes) 🎤
- Myanmar Singers Build 1-4
- Roles: လွှမ်းပိုင်, Bobby Soxer, Sai Sai, Yung Hugo, etc.

### 2. Random Selection
- Game တိုင်းမှာ theme က random ရွေးချယ်သွားမှာပါ
- Theme ရဲ့ emoji နဲ့ name က team announcement message မှာ ပြသပါတယ်
- ဥပမာ: "👑 Theme: Kingdom Build 2"

### 3. Theme-Based Roles
- Theme တိုင်းမှာ 5 rounds အတွက် 5 different roles ရှိပါတယ်
- Role names နဲ့ descriptions တွေက theme နဲ့ ညီညွတ်ပါတယ်
- MBTI-based scoring system က role အားလုံး အတွက် လုပ်ဆောင်ပါတယ်

### 4. Database Storage
- Theme ID က `games` table မှာ သိမ်းဆည်းထားပါတယ်
- Game ပြန် load လုပ်ရင်လည်း theme က correct ဖြစ်နေပါလိမ့်မယ်

## Implementation Details

### Files Added
1. **`data/themes.py`** - Theme definitions with 29 themes
2. **`database/add_theme_migration.sql`** - Database migration script

### Files Modified
1. **`database/db_manager.py`**
   - Added `theme_id` column to `games` table
   - Added `theme_id` parameter to `create_game()`
   - Added `get_game_theme()` method

2. **`handlers/game_handler.py`**
   - Added `game_themes` dictionary to store themes in memory
   - Random theme selection in `start_game()`
   - Theme announcement in team message
   - Replace `ROLES` with theme-based roles in `run_round()` and `announce_round_results()`

3. **`handlers/voting_handler.py`**
   - Replace `ROLES` with theme-based roles in:
     - `send_team_voting()`
     - `handle_vote()`
     - `finalize_voting()`

4. **`services/scoring_service.py`**
   - Replace `ROLES` with theme-based roles in `calculate_team_scores()`

### Database Schema
```sql
ALTER TABLE games 
ADD COLUMN IF NOT EXISTS theme_id INTEGER DEFAULT 1;
```

## Usage Example

### Game Flow
1. **Lobby Opens**: Players join
2. **Game Starts**: Random theme selected
3. **Team Announcement**: 
```
👑 Theme: Kingdom Build 2

🎮 TEAMS FORMED

Team 1: Alpha
- @user1
- @user2
- @user3

Team 2: Beta
- @user4
- @user5
- @user6
```

4. **Round 1**: Role from theme (e.g., "ဘုရင်" if Kingdom, "Superman" if DC)
5. **Round 2-5**: Continue with theme-specific roles

## Testing

### Test Random Theme Selection
```python
from data.themes import get_random_theme, get_theme_count

print(f"Total themes: {get_theme_count()}")  # Should print 29
theme = get_random_theme()
print(f"Selected: {theme['emoji']} {theme['name']}")
print(f"Roles: {list(theme['roles'].keys())}")
```

### Test Database Migration
```bash
# Run migration (if needed)
psql -d your_database -f database/add_theme_migration.sql
```

### Test Game with Theme
1. Start a new game (`/newgame`)
2. Check team announcement - should show theme
3. Check round messages - should show theme-specific role names
4. Check final scores - should calculate correctly with new roles

## Benefits

1. **Variety**: 29 different themes keep games fresh and exciting
2. **Replayability**: Players want to play again to experience different themes
3. **Cultural Relevance**: Myanmar singers, family roles resonate with local players
4. **Global Appeal**: DC, Marvel, Football themes attract international players
5. **Balanced**: All themes use same MBTI scoring system for fairness

## Future Enhancements

Potential additions:
- Season-based themes (Thingyan, Christmas, etc.)
- Player voting for theme preference
- Theme statistics (most won, most played)
- Custom themes created by admins
- Theme achievements/badges

## Notes

- Default theme is ID 1 (Kingdom Build) for backward compatibility
- All 29 themes have equal probability of selection
- Theme selection happens once per game (not per round)
- Themes are stored in database for persistence
- Memory cache (`game_themes`) used for performance

---

**Version**: 1.0  
**Date**: October 24, 2025  
**Total Themes**: 29  
**Categories**: 8

