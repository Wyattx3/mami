"""
Database Migration Script
Adds is_leader column to existing game_players table
"""
import asyncio
import sys
import sqlite3
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

async def migrate_database():
    """Add is_leader column to game_players table"""
    db_path = 'database/game.db'
    
    print("=" * 60)
    print("Database Migration: Adding is_leader Column")
    print("=" * 60)
    
    try:
        # Use synchronous sqlite3 for migration
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(game_players)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'is_leader' in columns:
            print("✅ is_leader column already exists!")
            conn.close()
            return
        
        print("🔧 Adding is_leader column to game_players table...")
        
        # Add the column
        cursor.execute('''
            ALTER TABLE game_players 
            ADD COLUMN is_leader INTEGER DEFAULT 0
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ Migration completed successfully!")
        print("\nColumn 'is_leader' added to game_players table.")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        print("\n" + "=" * 60)
        print("Alternative Solution:")
        print("=" * 60)
        print("Delete the database file and restart the bot:")
        print("  rm database/game.db")
        print("  python bot.py")
        print("\nThe bot will recreate the database with the correct schema.")
        print("=" * 60)
        return

    print("\n" + "=" * 60)
    print("Migration Complete!")
    print("=" * 60)
    print("You can now restart the bot:")
    print("  python bot.py")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(migrate_database())

