#!/usr/bin/env python3
"""
Comprehensive Test Suite for New Implementation
Tests: Random Theme System + Pre-defined Descriptions
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

import logging
from database.db_manager import db_manager
from data.themes import get_random_theme, get_theme_by_id, get_theme_count, THEMES
from handlers.voting_handler import get_character_description, MBTI_DESCRIPTIONS, ZODIAC_DESCRIPTIONS
from services.scoring_service import scoring_service
from models.character import Character
import config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TestResults:
    """Track test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_pass(self, test_name: str, message: str = ""):
        self.passed += 1
        self.tests.append(("✅", test_name, message))
        logger.info(f"✅ PASS: {test_name} - {message}")
    
    def add_fail(self, test_name: str, error: str = ""):
        self.failed += 1
        self.tests.append(("❌", test_name, error))
        logger.error(f"❌ FAIL: {test_name} - {error}")
    
    def print_summary(self):
        print("\n" + "="*80)
        print("📊 TEST SUMMARY")
        print("="*80)
        
        for status, name, msg in self.tests:
            print(f"{status} {name}")
            if msg:
                print(f"   → {msg}")
        
        print("\n" + "="*80)
        total = self.passed + self.failed
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"Success Rate: {(self.passed/total*100):.1f}%")
        print("="*80)
        
        return self.failed == 0


async def test_theme_system(results: TestResults):
    """Test 1: Theme System"""
    print("\n🎮 Test 1: Random Theme System")
    print("-" * 80)
    
    try:
        # Test 1.1: Theme count
        count = get_theme_count()
        if count == 29:
            results.add_pass("Theme Count", f"Found {count} themes")
        else:
            results.add_fail("Theme Count", f"Expected 29, got {count}")
        
        # Test 1.2: Random theme selection
        theme = get_random_theme()
        if theme and 'id' in theme and 'name' in theme and 'emoji' in theme:
            results.add_pass("Random Theme Selection", f"{theme['emoji']} {theme['name']}")
        else:
            results.add_fail("Random Theme Selection", "Invalid theme structure")
        
        # Test 1.3: Theme by ID
        theme_1 = get_theme_by_id(1)
        if theme_1 and theme_1['name'] == 'Kingdom Build':
            results.add_pass("Theme by ID", f"Loaded {theme_1['name']}")
        else:
            results.add_fail("Theme by ID", "Failed to load theme ID 1")
        
        # Test 1.4: Theme roles
        if theme_1 and 'roles' in theme_1 and len(theme_1['roles']) == 5:
            role_names = [theme_1['roles'][i]['name'] for i in range(1, 6)]
            results.add_pass("Theme Roles", f"5 roles: {', '.join(role_names)}")
        else:
            results.add_fail("Theme Roles", "Invalid roles structure")
        
        # Test 1.5: All themes have 5 roles
        all_valid = True
        for theme_id, theme_data in THEMES.items():
            if len(theme_data['roles']) != 5:
                all_valid = False
                break
        
        if all_valid:
            results.add_pass("All Themes Validation", "All 29 themes have 5 roles")
        else:
            results.add_fail("All Themes Validation", "Some themes missing roles")
        
        # Test 1.6: Theme categories
        categories = set(theme['category'] for theme in THEMES.values())
        expected = {'kingdom', 'family', 'friendship', 'relationship', 'superhero', 'sports', 'music'}
        if categories == expected:
            results.add_pass("Theme Categories", f"Found {len(categories)} categories")
        else:
            results.add_fail("Theme Categories", f"Expected {expected}, got {categories}")
        
    except Exception as e:
        results.add_fail("Theme System", f"Exception: {str(e)}")


async def test_pre_defined_descriptions(results: TestResults):
    """Test 2: Pre-defined Descriptions"""
    print("\n📝 Test 2: Pre-defined Descriptions (No AI)")
    print("-" * 80)
    
    try:
        # Test 2.1: MBTI descriptions count
        if len(MBTI_DESCRIPTIONS) == 16:
            results.add_pass("MBTI Descriptions", "All 16 types defined")
        else:
            results.add_fail("MBTI Descriptions", f"Expected 16, got {len(MBTI_DESCRIPTIONS)}")
        
        # Test 2.2: Zodiac descriptions count
        if len(ZODIAC_DESCRIPTIONS) == 12:
            results.add_pass("Zodiac Descriptions", "All 12 signs defined")
        else:
            results.add_fail("Zodiac Descriptions", f"Expected 12, got {len(ZODIAC_DESCRIPTIONS)}")
        
        # Test 2.3: Character description generation
        test_char = Character(
            id=1,
            name="Test User",
            mbti="INTJ",
            zodiac="Scorpio",
            description=""
        )
        
        desc = get_character_description(test_char)
        if desc and len(desc) > 0:
            results.add_pass("Character Description", f"Generated: {desc}")
        else:
            results.add_fail("Character Description", "Empty description")
        
        # Test 2.4: Test all MBTI types
        all_mbti_valid = True
        for mbti in MBTI_DESCRIPTIONS.keys():
            test_char = Character(id=1, name="Test", mbti=mbti, zodiac="Aries", description="")
            desc = get_character_description(test_char)
            if not desc or len(desc) < 10:
                all_mbti_valid = False
                break
        
        if all_mbti_valid:
            results.add_pass("All MBTI Descriptions", "All 16 types working")
        else:
            results.add_fail("All MBTI Descriptions", "Some types failed")
        
        # Test 2.5: Test all Zodiac signs
        all_zodiac_valid = True
        for zodiac in ZODIAC_DESCRIPTIONS.keys():
            test_char = Character(id=1, name="Test", mbti="INTJ", zodiac=zodiac, description="")
            desc = get_character_description(test_char)
            if not desc or len(desc) < 10:
                all_zodiac_valid = False
                break
        
        if all_zodiac_valid:
            results.add_pass("All Zodiac Descriptions", "All 12 signs working")
        else:
            results.add_fail("All Zodiac Descriptions", "Some signs failed")
        
        # Test 2.6: Unknown MBTI/Zodiac fallback
        test_char = Character(id=1, name="Test", mbti="XXXX", zodiac="Unknown", description="")
        desc = get_character_description(test_char)
        if desc:
            results.add_pass("Fallback Descriptions", "Handles unknown types gracefully")
        else:
            results.add_fail("Fallback Descriptions", "No fallback for unknown types")
        
    except Exception as e:
        results.add_fail("Pre-defined Descriptions", f"Exception: {str(e)}")


async def test_scoring_system(results: TestResults):
    """Test 3: Scoring System"""
    print("\n📊 Test 3: Pre-defined Scoring System")
    print("-" * 80)
    
    try:
        # Test 3.1: Character score calculation
        test_char = Character(
            id=1,
            name="Test Leader",
            mbti="ENTJ",
            zodiac="Leo",
            description=""
        )
        
        # Score for King role (should be high for ENTJ + Leo)
        score, explanation = scoring_service.calculate_character_score(test_char, "ဘုရင်")
        
        if 8 <= score <= 10:
            results.add_pass("Leader Scoring", f"ENTJ + Leo = {score}/10 (High)")
        else:
            results.add_fail("Leader Scoring", f"Expected 8-10, got {score}")
        
        # Test 3.2: Low score test
        test_char2 = Character(
            id=2,
            name="Test Introvert",
            mbti="INFP",
            zodiac="Pisces",
            description=""
        )
        
        score2, explanation2 = scoring_service.calculate_character_score(test_char2, "ဘုရင်")
        
        if 1 <= score2 <= 4:
            results.add_pass("Low Score Test", f"INFP + Pisces = {score2}/10 (Low)")
        else:
            results.add_fail("Low Score Test", f"Expected 1-4, got {score2}")
        
        # Test 3.3: Score range validation
        all_scores_valid = True
        for mbti in ['INTJ', 'ENTP', 'ISFJ', 'ESTP']:
            for zodiac in ['Aries', 'Cancer', 'Libra', 'Capricorn']:
                test_char = Character(id=1, name="Test", mbti=mbti, zodiac=zodiac, description="")
                score, _ = scoring_service.calculate_character_score(test_char, "ဘုရင်")
                if not (1 <= score <= 10):
                    all_scores_valid = False
                    break
        
        if all_scores_valid:
            results.add_pass("Score Range Validation", "All scores between 1-10")
        else:
            results.add_fail("Score Range Validation", "Some scores out of range")
        
        # Test 3.4: Explanation generation
        if explanation and len(explanation) > 0:
            results.add_pass("Score Explanation", "Explanation generated")
        else:
            results.add_fail("Score Explanation", "No explanation provided")
        
    except Exception as e:
        results.add_fail("Scoring System", f"Exception: {str(e)}")


async def test_database_integration(results: TestResults):
    """Test 4: Database Integration"""
    print("\n💾 Test 4: Database Integration")
    print("-" * 80)
    
    try:
        # Test 4.1: Database connection
        await db_manager.create_pool()
        results.add_pass("Database Connection", "Connected successfully")
        
        # Test 4.2: Database initialization
        await db_manager.init_database()
        results.add_pass("Database Initialization", "Tables initialized")
        
        # Test 4.3: Theme ID storage
        # Create a test game with theme
        game_id = await db_manager.create_game(
            lobby_message_id=999999,
            lobby_chat_id=999999,
            theme_id=5
        )
        
        if game_id:
            results.add_pass("Game Creation with Theme", f"Created game {game_id}")
        else:
            results.add_fail("Game Creation with Theme", "Failed to create game")
        
        # Test 4.4: Retrieve theme ID
        if game_id:
            theme_id = await db_manager.get_game_theme(game_id)
            if theme_id == 5:
                results.add_pass("Theme ID Retrieval", f"Retrieved theme {theme_id}")
            else:
                results.add_fail("Theme ID Retrieval", f"Expected 5, got {theme_id}")
            
            # Cleanup test game
            await db_manager.update_game_status(game_id, 'cancelled')
        
        # Test 4.5: Character database
        characters = await db_manager.get_all_characters()
        if len(characters) >= 40:
            results.add_pass("Character Database", f"Found {len(characters)} characters")
        else:
            results.add_fail("Character Database", f"Only {len(characters)} characters found")
        
    except Exception as e:
        results.add_fail("Database Integration", f"Exception: {str(e)}")


async def test_complete_flow(results: TestResults):
    """Test 5: Complete Game Flow Simulation"""
    print("\n🎲 Test 5: Complete Game Flow Simulation")
    print("-" * 80)
    
    try:
        # Step 1: Select random theme
        theme = get_random_theme()
        results.add_pass("Step 1: Theme Selection", f"{theme['emoji']} {theme['name']}")
        
        # Step 2: Create game with theme
        game_id = await db_manager.create_game(
            lobby_message_id=888888,
            lobby_chat_id=888888,
            theme_id=theme['id']
        )
        results.add_pass("Step 2: Game Creation", f"Game ID: {game_id}")
        
        # Step 3: Verify theme stored
        stored_theme_id = await db_manager.get_game_theme(game_id)
        if stored_theme_id == theme['id']:
            results.add_pass("Step 3: Theme Storage", "Theme ID matches")
        else:
            results.add_fail("Step 3: Theme Storage", "Theme ID mismatch")
        
        # Step 4: Simulate 5 rounds
        for round_num in 1, 2, 3, 4, 5:
            role_info = theme['roles'].get(round_num, {})
            role_name = role_info.get('name', 'Unknown')
            
            # Get test character
            characters = await db_manager.get_random_characters(1)
            if characters:
                char = characters[0]
                
                # Generate description (pre-defined)
                desc = get_character_description(char)
                
                # Calculate score (pre-defined)
                score, explanation = scoring_service.calculate_character_score(char, role_name)
                
                results.add_pass(
                    f"Step 4.{round_num}: Round {round_num}",
                    f"Role: {role_name}, Character: {char.name}, Score: {score}/10"
                )
        
        # Step 5: Cleanup
        await db_manager.update_game_status(game_id, 'cancelled')
        results.add_pass("Step 5: Cleanup", "Test game cancelled")
        
    except Exception as e:
        results.add_fail("Complete Game Flow", f"Exception: {str(e)}")


async def run_all_tests():
    """Run all tests"""
    print("\n" + "="*80)
    print("🧪 COMPREHENSIVE TEST SUITE")
    print("Testing: Random Theme System + Pre-defined Descriptions")
    print("="*80)
    
    results = TestResults()
    
    try:
        await test_theme_system(results)
        await test_pre_defined_descriptions(results)
        await test_scoring_system(results)
        await test_database_integration(results)
        await test_complete_flow(results)
        
    except Exception as e:
        logger.error(f"Test suite error: {e}")
        results.add_fail("Test Suite", str(e))
    
    finally:
        # Close database connection
        if db_manager.pool:
            await db_manager.pool.close()
            logger.info("Database connection closed")
    
    # Print summary
    success = results.print_summary()
    
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)

