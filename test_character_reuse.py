"""
Test Character Reuse Prevention
Verify that used characters are not reused in the same game
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from database.db_manager import db_manager
import config


class TestResults:
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self, test_name: str):
        self.total += 1
        self.passed += 1
        print(f"✅ PASS: {test_name}")
    
    def add_fail(self, test_name: str, reason: str):
        self.total += 1
        self.failed += 1
        self.errors.append((test_name, reason))
        print(f"❌ FAIL: {test_name}")
        print(f"   Reason: {reason}")
    
    def summary(self):
        print("\n" + "="*70)
        print("📊 TEST SUMMARY")
        print("="*70)
        print(f"Total Tests: {self.total}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"Success Rate: {(self.passed/self.total)*100:.1f}%")
        
        if self.errors:
            print("\n❌ Failed Tests:")
            for test_name, reason in self.errors:
                print(f"  - {test_name}: {reason}")
        
        print("="*70)


results = TestResults()


async def test_character_reuse_prevention():
    """Test that used characters are not reused in the same game"""
    print("\n🔄 Test: Character Reuse Prevention")
    print("="*70)
    
    # Setup: Create test game and team
    game_id = 99999
    team_id = 1
    
    print(f"\nTest Setup:")
    print(f"  Game ID: {game_id}")
    print(f"  Team ID: {team_id}")
    print(f"  Characters per round: {config.CHARACTERS_PER_VOTING}")
    
    # Test 1: Get random characters (no exclusions)
    print("\n📋 Test 1: Initial character selection (Round 1)")
    print("-" * 70)
    
    round1_chars = await db_manager.get_random_characters(
        config.CHARACTERS_PER_VOTING,
        exclude_ids=[]
    )
    
    round1_ids = [c.id for c in round1_chars]
    print(f"Round 1 Characters: {len(round1_chars)} selected")
    print(f"Character IDs: {round1_ids}")
    
    if len(round1_chars) == config.CHARACTERS_PER_VOTING:
        results.add_pass(f"Round 1: Got {config.CHARACTERS_PER_VOTING} characters")
    else:
        results.add_fail("Round 1 selection", f"Expected {config.CHARACTERS_PER_VOTING}, got {len(round1_chars)}")
    
    # Test 2: Get characters excluding Round 1 (simulate Round 2)
    print("\n📋 Test 2: Character selection with exclusion (Round 2)")
    print("-" * 70)
    
    # Simulate that team selected first character from Round 1
    used_char_id = round1_ids[0]
    print(f"Simulating: Team selected Character #{used_char_id} in Round 1")
    
    round2_chars = await db_manager.get_random_characters(
        config.CHARACTERS_PER_VOTING,
        exclude_ids=[used_char_id]
    )
    
    round2_ids = [c.id for c in round2_chars]
    print(f"Round 2 Characters: {len(round2_chars)} selected")
    print(f"Character IDs: {round2_ids}")
    
    # Check if used character is not in Round 2
    if used_char_id not in round2_ids:
        results.add_pass("Used character excluded from Round 2")
    else:
        results.add_fail("Exclusion", f"Character #{used_char_id} appeared again!")
    
    if len(round2_chars) == config.CHARACTERS_PER_VOTING:
        results.add_pass(f"Round 2: Got {config.CHARACTERS_PER_VOTING} new characters")
    else:
        results.add_fail("Round 2 selection", f"Expected {config.CHARACTERS_PER_VOTING}, got {len(round2_chars)}")
    
    # Test 3: Exclude multiple characters (simulate multiple rounds)
    print("\n📋 Test 3: Multiple character exclusions (Round 3-5)")
    print("-" * 70)
    
    # Simulate team has used 3 characters
    used_char_ids = round1_ids[:3]
    print(f"Simulating: Team used Characters {used_char_ids} in previous rounds")
    
    round3_chars = await db_manager.get_random_characters(
        config.CHARACTERS_PER_VOTING,
        exclude_ids=used_char_ids
    )
    
    round3_ids = [c.id for c in round3_chars]
    print(f"Round 3 Characters: {len(round3_chars)} selected")
    print(f"Character IDs: {round3_ids}")
    
    # Check no used characters appear
    overlap = set(round3_ids) & set(used_char_ids)
    if len(overlap) == 0:
        results.add_pass("All used characters excluded")
    else:
        results.add_fail("Multiple exclusion", f"Characters {overlap} reappeared!")
    
    # Test 4: Database function for getting used character IDs
    print("\n📋 Test 4: get_team_used_character_ids() function")
    print("-" * 70)
    
    # Insert test game round records
    async with db_manager.pool.acquire() as conn:
        # Clean up any existing test data
        await conn.execute('DELETE FROM game_rounds WHERE game_id = $1', game_id)
        await conn.execute('DELETE FROM games WHERE id = $1', game_id)
        
        # Create test game first (required for foreign key)
        await conn.execute('''
            INSERT INTO games (id, status, created_at, lobby_chat_id)
            VALUES ($1, $2, CURRENT_TIMESTAMP, $3)
        ''', game_id, 'active', -99999)
        
        # Insert test rounds
        test_used_chars = [10, 15, 20]
        for i, char_id in enumerate(test_used_chars, start=1):
            await conn.execute('''
                INSERT INTO game_rounds (game_id, round_number, team_id, role, selected_character_id)
                VALUES ($1, $2, $3, $4, $5)
            ''', game_id, i, team_id, f'Test Role {i}', char_id)
        
        print(f"Inserted test data: Team {team_id} used characters {test_used_chars}")
    
    # Get used character IDs
    retrieved_ids = await db_manager.get_team_used_character_ids(game_id, team_id)
    print(f"Retrieved used character IDs: {retrieved_ids}")
    
    if set(retrieved_ids) == set(test_used_chars):
        results.add_pass("get_team_used_character_ids() works correctly")
    else:
        results.add_fail("get_team_used_character_ids", 
                        f"Expected {test_used_chars}, got {retrieved_ids}")
    
    # Test 5: Full game simulation (5 rounds)
    print("\n📋 Test 5: Full game simulation (5 rounds)")
    print("-" * 70)
    
    all_used_chars = []
    
    for round_num in range(1, 6):
        chars = await db_manager.get_random_characters(
            config.CHARACTERS_PER_VOTING,
            exclude_ids=all_used_chars
        )
        
        char_ids = [c.id for c in chars]
        
        # Simulate team selects first character
        if chars:
            selected = char_ids[0]
            all_used_chars.append(selected)
            
            print(f"  Round {round_num}: Selected Character #{selected} from {char_ids}")
    
    print(f"\nAll selected characters: {all_used_chars}")
    print(f"Total unique characters used: {len(all_used_chars)}")
    
    # Check no duplicates
    if len(all_used_chars) == len(set(all_used_chars)):
        results.add_pass("No character reused across 5 rounds")
    else:
        duplicates = [c for c in all_used_chars if all_used_chars.count(c) > 1]
        results.add_fail("5-round simulation", f"Duplicates found: {set(duplicates)}")
    
    # Test 6: Check sufficient character pool
    print("\n📋 Test 6: Character pool size validation")
    print("-" * 70)
    
    total_chars = await db_manager.get_character_count()
    chars_needed = config.CHARACTERS_PER_VOTING * 5  # 5 rounds
    
    print(f"Total characters in DB: {total_chars}")
    print(f"Characters needed for 5 rounds: {chars_needed}")
    print(f"Buffer: {total_chars - chars_needed}")
    
    if total_chars >= chars_needed:
        results.add_pass(f"Sufficient characters ({total_chars} >= {chars_needed})")
    else:
        results.add_fail("Character pool", 
                        f"Not enough characters: {total_chars} < {chars_needed}")
    
    # Cleanup
    async with db_manager.pool.acquire() as conn:
        await conn.execute('DELETE FROM game_rounds WHERE game_id = $1', game_id)
        await conn.execute('DELETE FROM games WHERE id = $1', game_id)
    
    print("\n✅ Test cleanup completed")


async def test_exclusion_edge_cases():
    """Test edge cases for character exclusion"""
    print("\n🔍 Test: Exclusion Edge Cases")
    print("="*70)
    
    # Test 1: Empty exclusion list
    print("\n📋 Test 1: Empty exclusion list")
    print("-" * 70)
    
    chars = await db_manager.get_random_characters(5, exclude_ids=[])
    
    if len(chars) == 5:
        results.add_pass("Empty exclusion list works")
    else:
        results.add_fail("Empty exclusion", f"Expected 5, got {len(chars)}")
    
    # Test 2: None exclusion list
    print("\n📋 Test 2: None exclusion list")
    print("-" * 70)
    
    chars = await db_manager.get_random_characters(5, exclude_ids=None)
    
    if len(chars) == 5:
        results.add_pass("None exclusion list works")
    else:
        results.add_fail("None exclusion", f"Expected 5, got {len(chars)}")
    
    # Test 3: Large exclusion list
    print("\n📋 Test 3: Large exclusion list")
    print("-" * 70)
    
    total_chars = await db_manager.get_character_count()
    
    # Exclude many characters
    exclude_many = list(range(1, 30))  # Exclude first 29 characters
    chars = await db_manager.get_random_characters(5, exclude_ids=exclude_many)
    
    char_ids = [c.id for c in chars]
    overlap = set(char_ids) & set(exclude_many)
    
    print(f"Excluded {len(exclude_many)} characters")
    print(f"Got {len(chars)} characters: {char_ids}")
    
    if len(overlap) == 0 and len(chars) == 5:
        results.add_pass("Large exclusion list works")
    else:
        results.add_fail("Large exclusion", f"Overlap: {overlap}, Count: {len(chars)}")


async def main():
    """Run all character reuse tests"""
    print("="*70)
    print("🔄 CHARACTER REUSE PREVENTION TEST SUITE")
    print("="*70)
    print("\nTesting that used characters are not reused in same game...\n")
    
    try:
        # Connect to database
        await db_manager.create_pool()
        await db_manager.init_database()
        
        # Run tests
        await test_character_reuse_prevention()
        await test_exclusion_edge_cases()
        
        # Show summary
        results.summary()
        
        # Cleanup
        if db_manager.pool:
            await db_manager.close_pool()
        
        return 0 if results.failed == 0 else 1
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

