"""
Test PostgreSQL Database Connection
Quick script to verify Neon database connection works
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from database.db_manager import db_manager
from models.character import Character
import config


async def test_connection():
    """Test database connection and basic operations"""
    print("=" * 60)
    print("PostgreSQL/Neon Database Connection Test")
    print("=" * 60)
    
    try:
        # 1. Create connection pool
        print("\n🔌 Creating connection pool...")
        await db_manager.create_pool()
        print("✅ Connection pool created successfully!")
        
        # 2. Initialize database schema
        print("\n📋 Creating database tables...")
        await db_manager.init_database()
        print("✅ Database tables created successfully!")
        
        # 3. Test character count
        print("\n🔢 Checking character count...")
        count = await db_manager.get_character_count()
        print(f"✅ Found {count} characters in database")
        
        # 4. Test adding a character (if none exist)
        if count == 0:
            print("\n➕ Adding test character...")
            test_char = Character(
                name="Test Character",
                mbti="INTJ",
                zodiac="Aries",
                description="Test character",
                personality_traits="test"
            )
            char_id = await db_manager.add_character(test_char)
            print(f"✅ Test character added with ID: {char_id}")
            
            # Verify it was added
            count = await db_manager.get_character_count()
            print(f"✅ New character count: {count}")
        
        # 5. Test getting all characters
        print("\n📖 Fetching all characters...")
        characters = await db_manager.get_all_characters()
        print(f"✅ Retrieved {len(characters)} characters:")
        for char in characters:
            print(f"   - {char.name} (MBTI: {char.mbti}, Zodiac: {char.zodiac})")
        
        # 6. Test lobby operations
        print("\n🏠 Testing lobby operations...")
        lobby_count = await db_manager.get_lobby_count()
        print(f"✅ Current lobby count: {lobby_count}")
        
        print("\n" + "=" * 60)
        print("🎉 All tests passed successfully!")
        print("=" * 60)
        print("\n✅ Database connection is working properly")
        print(f"✅ Database URL: {config.DATABASE_URL[:50]}...")
        print("\n🚀 You can now run the bot with: python bot.py")
        print("=" * 60)
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ Database Connection Test Failed!")
        print("=" * 60)
        print(f"\nError: {type(e).__name__}: {e}")
        print("\n" + "=" * 60)
        print("Troubleshooting:")
        print("=" * 60)
        print("1. Check DATABASE_URL in .env file")
        print("2. Verify Neon database is accessible")
        print("3. Check network/firewall settings")
        print("4. Ensure asyncpg is installed:")
        print("   pip install asyncpg")
        print("=" * 60)
        sys.exit(1)
    
    finally:
        # Close connection pool
        print("\n🔌 Closing connection pool...")
        await db_manager.close_pool()
        print("✅ Connection pool closed")


if __name__ == "__main__":
    asyncio.run(test_connection())

