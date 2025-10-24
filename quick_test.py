#!/usr/bin/env python3
"""
Quick Interactive Test - Check if bot is configured correctly
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import logging
from database.db_manager import db_manager
from data.themes import get_random_theme, get_theme_count
from handlers.voting_handler import get_character_description
from models.character import Character
import config

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


async def quick_test():
    """Quick test of main features"""
    print("\n" + "="*70)
    print("🎮 QUICK BOT FEATURE TEST")
    print("="*70 + "\n")
    
    # Test 1: Configuration
    print("📝 Test 1: Configuration")
    print("-" * 70)
    if config.TELEGRAM_BOT_TOKEN:
        print(f"✅ Bot Token: {'*' * 20}{config.TELEGRAM_BOT_TOKEN[-10:]}")
    else:
        print("❌ Bot Token: NOT SET!")
        return False
    
    if config.DATABASE_URL:
        print(f"✅ Database URL: Configured")
    else:
        print("❌ Database URL: NOT SET!")
        return False
    
    print(f"✅ Polling Mode: {not config.USE_WEBHOOK}")
    print(f"✅ Min Players: {config.MIN_PLAYERS}")
    print(f"✅ Max Players: {config.MAX_PLAYERS}")
    print(f"✅ Team Size: {config.TEAM_SIZE}")
    
    # Test 2: Theme System
    print(f"\n📚 Test 2: Theme System")
    print("-" * 70)
    theme_count = get_theme_count()
    print(f"✅ Total Themes: {theme_count}")
    
    theme = get_random_theme()
    print(f"✅ Random Theme: {theme['emoji']} {theme['name']}")
    print(f"   Category: {theme['category']}")
    print(f"   Roles:")
    for i in range(1, 6):
        role = theme['roles'][i]
        print(f"   Round {i}: {role['name']} - {role['description']}")
    
    # Test 3: Character Descriptions
    print(f"\n👤 Test 3: Character Descriptions")
    print("-" * 70)
    test_chars = [
        ("ENTJ", "Leo", "ခေါင်းဆောင် (High Score)"),
        ("INFP", "Pisces", "အနုပညာရှင် (Low Score)"),
        ("ISTP", "Scorpio", "လက်တွေ့ကျသူ"),
    ]
    
    for mbti, zodiac, desc_type in test_chars:
        char = Character(1, f"Test {mbti}", mbti, zodiac, "")
        description = get_character_description(char)
        print(f"✅ {mbti} + {zodiac} ({desc_type})")
        print(f"   → {description}")
    
    # Test 4: Database
    print(f"\n💾 Test 4: Database Connection")
    print("-" * 70)
    try:
        await db_manager.create_pool()
        print("✅ Database connected")
        
        characters = await db_manager.get_all_characters()
        print(f"✅ Characters in DB: {len(characters)}")
        
        if len(characters) >= 3:
            print(f"   Sample characters:")
            for char in characters[:3]:
                print(f"   - {char.name} ({char.mbti} {char.zodiac})")
        
        await db_manager.pool.close()
        print("✅ Database connection closed")
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    # Summary
    print(f"\n" + "="*70)
    print("✅ ALL CHECKS PASSED!")
    print("="*70)
    print(f"\n🚀 Bot is ready to start!")
    print(f"\nTo start the bot, run:")
    print(f"   python bot.py")
    print(f"\nThen in Telegram:")
    print(f"   1. Search for your bot")
    print(f"   2. Send /start")
    print(f"   3. Create a group and add the bot")
    print(f"   4. Send /newgame to start a lobby")
    print(f"   5. Players join the lobby")
    print(f"   6. Game starts automatically when conditions are met")
    print(f"\n" + "="*70 + "\n")
    
    return True


if __name__ == "__main__":
    success = asyncio.run(quick_test())
    sys.exit(0 if success else 1)

