"""
Add new character list to PostgreSQL database
Updated list with 40 characters
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from database.db_manager import db_manager
from models.character import Character


async def add_new_characters():
    """Add the new character list to database"""
    print("=" * 60)
    print("Adding New Characters to PostgreSQL")
    print("=" * 60)
    
    # New character list with MBTI and Zodiac
    characters_data = [
        ("Aye Thinn Kyu", "ISTJ", "Scorpio"),
        ("Aye Myat Swe", "ENFP", "Scorpio"),  # MBTI was missing, used ENFP from old list
        ("Aye Sin Sin Lin", "ISFP", "Aries"),
        ("Alvina Mine", "ENFJ", "Gemini"),
        ("Aung Khant Ko", "INFP", "Taurus"),
        ("Aye Chan Ko Ko", "ESTP", "Gemini"),
        ("Chifuu", "ISFJ", "Cancer"),
        ("Chuu", "ISFJ", "Virgo"),
        ("Dora Honey", "ISTJ", "Virgo"),
        ("Emilymore", "ENFP", "Taurus"),
        ("Gon Freecss", "INFJ", "Pisces"),
        ("Htet Lae Mon Soe", "ESFJ", "Sagittarius"),
        ("Htet Wai Yan", "ISTJ", "Gemini"),
        ("AhHnin", "ENFP", "Leo"),
        ("Jel Jel", "ISTP", "Cancer"),
        ("Kyaw Thiha Phyo", "ESTP", "Cancer"),
        ("Kyaw Htut Lynn", "ENTP", "Leo"),
        # Kyaw Su Thawy - skipped (no MBTI/Zodiac)
        ("Kay Kabyar", "INFJ", "Scorpio"),
        ("Kaythari", "ENFP", "Libra"),
        ("Lone", "ISTJ", "Taurus"),
        ("Luneth", "INTP", "Libra"),
        # Nang Shwe Yamin Oo - skipped (no MBTI/Zodiac)
        # Nay Ma Nyo - skipped (no MBTI/Zodiac)
        ("May Myat Noe Khin", "ISFJ", "Sagittarius"),
        ("Myo Zarni Kyaw", "ISFJ", "Taurus"),
        # Myat Min Thar - skipped (no MBTI/Zodiac)
        ("Maung Kaung", "ESTJ", "Virgo"),
        ("Myat Thura Kyaw", "INFJ", "Sagittarius"),
        ("Puddin", "ENFP", "Aries"),
        ("Phyoei", "ISFJ", "Taurus"),
        ("PhoneMyat Hein", "ESFP", "Pisces"),
        ("Sai Sai", "ESTP", "Scorpio"),
        # Thura Kaung Maw - skipped (no MBTI/Zodiac)
        ("Taffy", "ISTP", "Scorpio"),
        ("Wint", "ISFJ", "Aries"),
        ("Nay Waratt Paing", "ESTJ", "Aquarius"),
        ("Yu Ya Hlaing", "ISFJ", "Taurus"),
        ("Ya Mone", "INFJ", "Cancer"),
        ("Zue May Thaw", "INTJ", "Aquarius"),
    ]
    
    try:
        # Connect to database
        print("\n🔌 Connecting to PostgreSQL...")
        await db_manager.create_pool()
        print("✅ Connected")
        
        # Initialize tables (if not exists)
        await db_manager.init_database()
        
        # Check existing characters
        existing_count = await db_manager.get_character_count()
        print(f"\n📊 Current character count: {existing_count}")
        
        # Get existing character names to check for duplicates
        existing_chars = await db_manager.get_all_characters()
        existing_names = {char.name.lower() for char in existing_chars}
        
        # Add characters
        print(f"\n➕ Adding {len(characters_data)} new characters...")
        print("=" * 60)
        added = 0
        skipped = 0
        errors = 0
        
        for name, mbti, zodiac in characters_data:
            # Skip if already exists
            if name.lower() in existing_names:
                print(f"   ⏭️  {name} - Already exists")
                skipped += 1
                continue
            
            try:
                character = Character(
                    id=None,
                    name=name,
                    mbti=mbti,
                    zodiac=zodiac,
                    description=f"{name} - {mbti} personality with {zodiac} zodiac sign",
                    personality_traits=f"{mbti}_{zodiac}"
                )
                
                char_id = await db_manager.add_character(character)
                print(f"   ✅ {name} ({mbti}, {zodiac}) - ID: {char_id}")
                added += 1
                
            except Exception as e:
                if 'unique' in str(e).lower() or 'duplicate' in str(e).lower():
                    print(f"   ⏭️  {name} - Duplicate, skipped")
                    skipped += 1
                else:
                    print(f"   ❌ Error: {name} - {e}")
                    errors += 1
        
        # Final count
        final_count = await db_manager.get_character_count()
        
        print("\n" + "=" * 60)
        print("✅ Character Addition Complete!")
        print("=" * 60)
        print(f"➕ New characters added: {added}")
        if skipped > 0:
            print(f"⏭️  Skipped (duplicates): {skipped}")
        if errors > 0:
            print(f"❌ Errors: {errors}")
        print(f"📊 Total characters in database: {final_count}")
        print("=" * 60)
        
        # Show all characters
        if final_count > 0:
            print("\n📖 All Characters in Database:")
            print("-" * 60)
            all_chars = await db_manager.get_all_characters()
            for i, char in enumerate(all_chars, 1):
                print(f"{i:2d}. {char.name:30s} ({char.mbti:4s}, {char.zodiac})")
        
        print("\n🎮 Ready to play! Use /newgame in Telegram group")
        
    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        await db_manager.close_pool()
        print("\n🔌 Connection closed")


if __name__ == "__main__":
    print("\n⚠️  Note: Characters without MBTI/Zodiac data are skipped:")
    print("   - Kyaw Su Thawy")
    print("   - Nang Shwe Yamin Oo")
    print("   - Nay Ma Nyo")
    print("   - Myat Min Thar")
    print("   - Thura Kaung Maw")
    print(f"\n✅ Will add {36} characters with complete data\n")
    
    asyncio.run(add_new_characters())

