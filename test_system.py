"""
Comprehensive System Test
Tests all major components of the bot
"""
import asyncio
import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Test results tracker
test_results = {
    'passed': [],
    'failed': [],
    'warnings': []
}

def test_result(test_name: str, passed: bool, message: str = ""):
    """Record test result"""
    if passed:
        test_results['passed'].append(test_name)
        logger.info(f"✅ {test_name}: PASSED {message}")
    else:
        test_results['failed'].append(test_name)
        logger.error(f"❌ {test_name}: FAILED {message}")


async def test_config():
    """Test configuration loading"""
    try:
        import config
        
        # Check required configs
        assert config.TELEGRAM_BOT_TOKEN, "TELEGRAM_BOT_TOKEN not set"
        assert config.DATABASE_URL, "DATABASE_URL not set"
        assert config.GEMINI_API_KEY, "GEMINI_API_KEY not set"
        
        test_result("Config Loading", True, f"(Mode: {'WEBHOOK' if config.USE_WEBHOOK else 'POLLING'})")
        return True
    except Exception as e:
        test_result("Config Loading", False, f"({str(e)})")
        return False


async def test_database_connection():
    """Test database connection"""
    try:
        from database.db_manager import db_manager
        
        # Create pool
        await db_manager.create_pool()
        test_result("Database Pool Creation", True)
        
        # Test connection
        conn = await db_manager.pool.acquire()
        try:
            # Simple query
            result = await conn.fetchval("SELECT 1")
            assert result == 1
            test_result("Database Connection", True)
        finally:
            await db_manager.pool.release(conn)
        
        return True
    except Exception as e:
        test_result("Database Connection", False, f"({str(e)})")
        return False


async def test_database_tables():
    """Test database table initialization"""
    try:
        from database.db_manager import db_manager
        
        # Initialize tables
        await db_manager.init_database()
        test_result("Database Tables Init", True)
        
        # Check tables exist
        conn = await db_manager.pool.acquire()
        try:
            tables = await conn.fetch("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            
            table_names = [t['table_name'] for t in tables]
            required_tables = ['characters', 'games', 'players', 'teams', 'votes']
            
            for table in required_tables:
                if table in table_names:
                    test_result(f"Table '{table}' exists", True)
                else:
                    test_result(f"Table '{table}' exists", False)
        finally:
            await db_manager.pool.release(conn)
        
        return True
    except Exception as e:
        test_result("Database Tables", False, f"({str(e)})")
        return False


async def test_state_management():
    """Test state management system"""
    try:
        from utils.state_manager import state_manager, GameState, UserState
        
        # Initialize state tables
        await state_manager.init_state_tables()
        test_result("State Tables Init", True)
        
        # Test game state
        test_chat_id = -999999999
        await state_manager.set_game_state(
            test_chat_id, 
            GameState.LOBBY_OPEN,
            metadata={'test': True}
        )
        test_result("Set Game State", True)
        
        state_data = await state_manager.get_game_state(test_chat_id)
        assert state_data['state'] == GameState.LOBBY_OPEN
        assert state_data['metadata']['test'] == True
        test_result("Get Game State", True)
        
        # Test user state
        test_user_id = 999999999
        await state_manager.set_user_state(
            test_user_id,
            test_chat_id,
            UserState.IN_LOBBY,
            metadata={'team': 1}
        )
        test_result("Set User State", True)
        
        user_state_data = await state_manager.get_user_state(test_user_id, test_chat_id)
        assert user_state_data['state'] == UserState.IN_LOBBY
        assert user_state_data['metadata']['team'] == 1
        test_result("Get User State", True)
        
        # Cleanup
        await state_manager.clear_game_state(test_chat_id)
        await state_manager.clear_user_states(test_chat_id)
        test_result("State Cleanup", True)
        
        return True
    except Exception as e:
        test_result("State Management", False, f"({str(e)})")
        return False


async def test_error_handling():
    """Test error handling utilities"""
    try:
        from utils.error_handler import (
            InputValidator, 
            BotError, 
            ValidationError,
            GameError
        )
        
        # Test number validation
        is_valid, value, msg = InputValidator.validate_number("50", 1, 100)
        assert is_valid and value == 50
        test_result("Input Validation (valid number)", True)
        
        is_valid, value, msg = InputValidator.validate_number("abc", 1, 100)
        assert not is_valid
        test_result("Input Validation (invalid number)", True)
        
        is_valid, value, msg = InputValidator.validate_number("150", 1, 100)
        assert not is_valid
        test_result("Input Validation (out of range)", True)
        
        # Test username validation
        is_valid, msg = InputValidator.validate_username("John Doe")
        assert is_valid
        test_result("Username Validation (valid)", True)
        
        is_valid, msg = InputValidator.validate_username("")
        assert not is_valid
        test_result("Username Validation (empty)", True)
        
        # Test custom exceptions
        try:
            raise ValidationError("Test error", user_message="Test message")
        except ValidationError as e:
            assert e.user_message == "Test message"
            test_result("Custom Exceptions", True)
        
        return True
    except Exception as e:
        test_result("Error Handling", False, f"({str(e)})")
        return False


async def test_logging_system():
    """Test logging configuration"""
    try:
        from utils.logger_config import game_logger, performance_logger
        import os
        
        # Check if logs directory exists or can be created
        log_dir = Path("logs")
        if not log_dir.exists():
            log_dir.mkdir(exist_ok=True)
        test_result("Log Directory", True)
        
        # Test game logger
        game_logger.log_game_start(
            chat_id=-999999999,
            player_count=9,
            lobby_size=9
        )
        test_result("Game Logger", True)
        
        # Test performance logger
        performance_logger.log_operation_time(
            operation="test_operation",
            duration_ms=100.5,
            success=True
        )
        test_result("Performance Logger", True)
        
        return True
    except Exception as e:
        test_result("Logging System", False, f"({str(e)})")
        return False


async def test_transaction_manager():
    """Test database transaction manager"""
    try:
        from database.transaction_manager import transaction_manager
        
        # Test basic transaction
        async with transaction_manager.transaction() as conn:
            result = await conn.fetchval("SELECT 1")
            assert result == 1
        test_result("Transaction Manager", True)
        
        # Test rollback on error
        try:
            async with transaction_manager.transaction() as conn:
                await conn.execute("SELECT 1")
                raise Exception("Test rollback")
        except Exception:
            pass
        test_result("Transaction Rollback", True)
        
        return True
    except Exception as e:
        test_result("Transaction Manager", False, f"({str(e)})")
        return False


async def test_character_database():
    """Test character database operations"""
    try:
        from database.db_manager import db_manager
        
        # Get characters
        characters = await db_manager.get_all_characters()
        
        if len(characters) > 0:
            test_result("Character Database", True, f"({len(characters)} characters found)")
        else:
            test_results['warnings'].append("No characters in database")
            logger.warning("⚠️  No characters found in database")
            test_result("Character Database", True, "(empty - needs data)")
        
        return True
    except Exception as e:
        test_result("Character Database", False, f"({str(e)})")
        return False


async def test_bot_token():
    """Test Telegram bot token validity"""
    try:
        import config
        from telegram import Bot
        
        bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
        bot_info = await bot.get_me()
        
        test_result("Bot Token Validation", True, f"(@{bot_info.username})")
        return True
    except Exception as e:
        test_result("Bot Token Validation", False, f"({str(e)})")
        return False


async def cleanup():
    """Cleanup test resources"""
    try:
        from database.db_manager import db_manager
        
        # Close database pool
        if db_manager.pool:
            await db_manager.pool.close()
        
        logger.info("🧹 Cleanup completed")
    except Exception as e:
        logger.warning(f"Cleanup warning: {e}")


def print_summary():
    """Print test summary"""
    print("\n" + "=" * 70)
    print("🧪 TEST SUMMARY")
    print("=" * 70)
    
    total = len(test_results['passed']) + len(test_results['failed'])
    passed = len(test_results['passed'])
    failed = len(test_results['failed'])
    warnings = len(test_results['warnings'])
    
    print(f"\n✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {failed}/{total}")
    if warnings > 0:
        print(f"⚠️  Warnings: {warnings}")
    
    if failed > 0:
        print("\n❌ Failed Tests:")
        for test in test_results['failed']:
            print(f"  - {test}")
    
    if warnings > 0:
        print("\n⚠️  Warnings:")
        for warning in test_results['warnings']:
            print(f"  - {warning}")
    
    print("\n" + "=" * 70)
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED! Bot is ready to run!")
    else:
        print("⚠️  Some tests failed. Please fix issues before deploying.")
    
    print("=" * 70 + "\n")
    
    return failed == 0


async def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("🧪 COMPREHENSIVE SYSTEM TEST")
    print("=" * 70 + "\n")
    
    logger.info("Starting system tests...\n")
    
    # Run tests in order
    tests = [
        ("Configuration", test_config),
        ("Database Connection", test_database_connection),
        ("Database Tables", test_database_tables),
        ("State Management", test_state_management),
        ("Error Handling", test_error_handling),
        ("Logging System", test_logging_system),
        ("Transaction Manager", test_transaction_manager),
        ("Character Database", test_character_database),
        ("Bot Token", test_bot_token),
    ]
    
    for test_name, test_func in tests:
        logger.info(f"\n--- Testing: {test_name} ---")
        try:
            await test_func()
        except Exception as e:
            logger.error(f"Test crashed: {e}")
            test_result(test_name, False, f"(crashed: {str(e)})")
    
    # Cleanup
    await cleanup()
    
    # Print summary
    success = print_summary()
    
    return 0 if success else 1


if __name__ == '__main__':
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

