"""
Add real characters to PostgreSQL database
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from database.db_manager import db_manager
from models.character import Character


async def add_characters():
    """Add the 12 real characters to database"""
    print("=" * 60)
    print("Adding Real Characters to PostgreSQL")
    print("=" * 60)
    
    characters_data = [
        ("Dabi", "ESTJ", "Pisces"),
        ("Aung Khant Kyaw", "INFP", "Taurus"),
        ("Nang Kaythiri", "ENFP", "Libra"),
        ("Luneth", "INTP", "Libra"),
        ("Maung Kaung", "ESTJ", "Virgo"),
        ("Nay Waratt Paing", "ESTJ", "Aquarius"),
        ("Jerry", "ISTP", "Cancer"),
        ("Phyo Ei", "ISFJ", "Taurus"),
        ("Aye Myat Swe", "ENFP", "Scorpio"),
        ("Wint", "ISFJ", "Aries"),
        ("Yamone", "INFJ", "Cancer"),
        ("Sai Sai Lu Wine", "ESTP", "Scorpio"),
    ]
    
    try:
        # Connect to database
        print("\n🔌 Connecting to PostgreSQL...")
        await db_manager.create_pool()
        print("✅ Connected")
        
        # Initialize tables
        await db_manager.init_database()
        
        # Check existing characters
        existing_count = await db_manager.get_character_count()
        print(f"\n📊 Current character count: {existing_count}")
        
        # Add characters
        print("\n➕ Adding characters...")
        added = 0
        skipped = 0
        
        for name, mbti, zodiac in characters_data:
            try:
                character = Character(
                    id=None,
                    name=name,
                    mbti=mbti,
                    zodiac=zodiac,
                    description=f"{name} - {mbti} personality with {zodiac} zodiac",
                    personality_traits=f"{mbti}_{zodiac}"
                )
                
                char_id = await db_manager.add_character(character)
                print(f"   ✅ {name} (MBTI: {mbti}, Zodiac: {zodiac}) - ID: {char_id}")
                added += 1
                
            except Exception as e:
                if 'unique' in str(e).lower() or 'duplicate' in str(e).lower():
                    print(f"   ⏭️  {name} - Already exists, skipped")
                    skipped += 1
                else:
                    print(f"   ❌ Error adding {name}: {e}")
        
        # Final count
        final_count = await db_manager.get_character_count()
        
        print("\n" + "=" * 60)
        print("✅ Characters Added Successfully!")
        print("=" * 60)
        print(f"➕ New characters added: {added}")
        if skipped > 0:
            print(f"⏭️  Skipped (already exist): {skipped}")
        print(f"📊 Total characters in database: {final_count}")
        print("=" * 60)
        print("\n🎮 Ready to play! Use /newgame in Telegram group")
        
    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {e}")
        sys.exit(1)
    
    finally:
        await db_manager.close_pool()
        print("\n🔌 Connection closed")


if __name__ == "__main__":
    asyncio.run(add_characters())

