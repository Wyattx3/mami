#!/usr/bin/env python3
"""
Run database migration to add theme_id column
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import logging
from database.db_manager import db_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_migration():
    """Run the theme_id migration"""
    try:
        # Connect to database
        await db_manager.create_pool()
        logger.info("✅ Database connected")
        
        # Run migration
        async with db_manager.pool.acquire() as conn:
            # Add theme_id column
            await conn.execute('''
                ALTER TABLE games 
                ADD COLUMN IF NOT EXISTS theme_id INTEGER DEFAULT 1
            ''')
            logger.info("✅ Added theme_id column to games table")
            
            # Add comment
            try:
                await conn.execute('''
                    COMMENT ON COLUMN games.theme_id IS 
                    'Theme ID from themes.py - determines role names for each round'
                ''')
                logger.info("✅ Added column comment")
            except Exception as e:
                logger.warning(f"⚠️ Could not add comment (non-critical): {e}")
            
            # Verify column exists
            result = await conn.fetchrow('''
                SELECT column_name, data_type, column_default 
                FROM information_schema.columns 
                WHERE table_name = 'games' AND column_name = 'theme_id'
            ''')
            
            if result:
                logger.info(f"✅ Verified: theme_id column exists")
                logger.info(f"   Type: {result['data_type']}, Default: {result['column_default']}")
            else:
                logger.error("❌ Column not found after migration!")
                return False
        
        logger.info("\n🎉 Migration completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        return False
    
    finally:
        if db_manager.pool:
            await db_manager.pool.close()
            logger.info("Database connection closed")


if __name__ == "__main__":
    success = asyncio.run(run_migration())
    sys.exit(0 if success else 1)

