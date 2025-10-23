"""
Migration Script: SQLite to PostgreSQL (Neon)
Migrates existing character data from SQLite to PostgreSQL
"""
import asyncio
import sqlite3
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from database.db_manager import db_manager
from models.character import Character
import config


async def migrate_characters():
    """Migrate characters from SQLite to PostgreSQL"""
    print("=" * 60)
    print("Database Migration: SQLite → PostgreSQL")
    print("=" * 60)
    
    # Check if SQLite database exists
    sqlite_path = config.DATABASE_PATH
    if not Path(sqlite_path).exists():
        print(f"\n❌ SQLite database not found at: {sqlite_path}")
        print("   No data to migrate. Skipping...")
        print("\n✅ You can proceed to add characters using /addcharacter")
        return
    
    print(f"\n📁 Found SQLite database: {sqlite_path}")
    
    try:
        # 1. Read characters from SQLite
        print("\n📖 Reading characters from SQLite...")
        sqlite_conn = sqlite3.connect(sqlite_path)
        sqlite_conn.row_factory = sqlite3.Row
        cursor = sqlite_conn.execute('SELECT * FROM characters')
        sqlite_rows = cursor.fetchall()
        sqlite_conn.close()
        
        print(f"✅ Found {len(sqlite_rows)} characters in SQLite")
        
        if len(sqlite_rows) == 0:
            print("\n⚠️  No characters to migrate")
            return
        
        # 2. Connect to PostgreSQL
        print("\n🔌 Connecting to PostgreSQL (Neon)...")
        await db_manager.create_pool()
        print("✅ Connected to PostgreSQL")
        
        # 3. Initialize PostgreSQL schema
        print("\n📋 Creating PostgreSQL tables...")
        await db_manager.init_database()
        print("✅ Tables created")
        
        # 4. Check existing characters in PostgreSQL
        existing_count = await db_manager.get_character_count()
        print(f"\n🔢 Existing characters in PostgreSQL: {existing_count}")
        
        # 5. Migrate characters
        print("\n🚀 Migrating characters...")
        migrated = 0
        skipped = 0
        
        for row in sqlite_rows:
            character = Character(
                name=row['name'],
                mbti=row['mbti'],
                zodiac=row['zodiac'],
                description=row['description'],
                personality_traits=row['personality_traits']
            )
            
            try:
                char_id = await db_manager.add_character(character)
                print(f"   ✅ Migrated: {character.name} (ID: {char_id})")
                migrated += 1
            except Exception as e:
                if 'unique' in str(e).lower() or 'duplicate' in str(e).lower():
                    print(f"   ⏭️  Skipped: {character.name} (already exists)")
                    skipped += 1
                else:
                    print(f"   ❌ Error migrating {character.name}: {e}")
        
        # 6. Verify migration
        final_count = await db_manager.get_character_count()
        print("\n" + "=" * 60)
        print("Migration Complete!")
        print("=" * 60)
        print(f"✅ Characters migrated: {migrated}")
        if skipped > 0:
            print(f"⏭️  Characters skipped (duplicates): {skipped}")
        print(f"📊 Total in PostgreSQL: {final_count}")
        print("=" * 60)
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ Migration Failed!")
        print("=" * 60)
        print(f"Error: {type(e).__name__}: {e}")
        print("\nPlease check:")
        print("1. DATABASE_URL is correctly set in .env")
        print("2. PostgreSQL database is accessible")
        print("3. SQLite database is not corrupted")
        sys.exit(1)
    
    finally:
        await db_manager.close_pool()
        print("\n🔌 Connection closed")


if __name__ == "__main__":
    print("\n⚠️  WARNING: This will copy characters from SQLite to PostgreSQL")
    print("   Existing PostgreSQL data will not be deleted")
    print("   Duplicate characters will be skipped")
    
    response = input("\nContinue? (yes/no): ").strip().lower()
    if response in ['yes', 'y']:
        asyncio.run(migrate_characters())
    else:
        print("\n❌ Migration cancelled")

