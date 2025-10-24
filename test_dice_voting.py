"""
Test Dice Voting with Team Voting System
Verify that dice votes work with majority voting logic
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from handlers.voting_handler import voting_handler
from database.db_manager import db_manager


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


async def test_dice_vote_resolution():
    """Test dice voting with team voting resolution"""
    print("\n🎲 Test: Dice Voting with Team Resolution")
    print("="*70)
    
    # Setup team players
    team_players = [
        {'user_id': 1001, 'username': 'Player1', 'is_leader': True},
        {'user_id': 1002, 'username': 'Player2', 'is_leader': False},
        {'user_id': 1003, 'username': 'Player3', 'is_leader': False}
    ]
    
    print("\nTeam Setup:")
    for p in team_players:
        leader_mark = "👑" if p['is_leader'] else "  "
        print(f"  {leader_mark} {p['username']} (ID: {p['user_id']})")
    
    # Test 1: All players vote for different characters (no dice)
    print("\n📋 Test 1: Normal voting - All different, leader wins")
    print("-" * 70)
    votes_1 = {
        1001: 10,  # Leader votes Character 10
        1002: 15,  # Player 2 votes Character 15
        1003: 20   # Player 3 votes Character 20
    }
    
    result_1 = voting_handler.resolve_team_vote(votes_1, team_players)
    print(f"Votes: Leader→#10, P2→#15, P3→#20")
    print(f"Result: Character #{result_1}")
    
    if result_1 == 10:
        results.add_pass("Leader vote wins when all different")
    else:
        results.add_fail("Leader vote", f"Expected 10, got {result_1}")
    
    # Test 2: Majority vote (2 same characters)
    print("\n📋 Test 2: Majority voting - 2 same characters win")
    print("-" * 70)
    votes_2 = {
        1001: 10,  # Leader votes Character 10
        1002: 15,  # Player 2 votes Character 15
        1003: 15   # Player 3 votes Character 15 (same as P2)
    }
    
    result_2 = voting_handler.resolve_team_vote(votes_2, team_players)
    print(f"Votes: Leader→#10, P2→#15, P3→#15")
    print(f"Result: Character #{result_2}")
    
    if result_2 == 15:
        results.add_pass("Majority vote wins (2 vs 1)")
    else:
        results.add_fail("Majority vote", f"Expected 15, got {result_2}")
    
    # Test 3: Dice vote with majority (dice loses)
    print("\n📋 Test 3: Dice vote + Majority - Majority wins")
    print("-" * 70)
    votes_3 = {
        1001: 23,  # Leader uses dice → Character 23 (random)
        1002: 30,  # Player 2 manually selects Character 30
        1003: 30   # Player 3 manually selects Character 30
    }
    
    result_3 = voting_handler.resolve_team_vote(votes_3, team_players)
    print(f"Votes: Leader(dice)→#23, P2(manual)→#30, P3(manual)→#30")
    print(f"Result: Character #{result_3}")
    
    if result_3 == 30:
        results.add_pass("Manual majority beats dice vote")
    else:
        results.add_fail("Dice vs majority", f"Expected 30, got {result_3}")
    
    # Test 4: All dice votes (different results)
    print("\n📋 Test 4: All dice votes - Leader's random wins")
    print("-" * 70)
    votes_4 = {
        1001: 5,   # Leader dice → Character 5
        1002: 12,  # Player 2 dice → Character 12
        1003: 18   # Player 3 dice → Character 18
    }
    
    result_4 = voting_handler.resolve_team_vote(votes_4, team_players)
    print(f"Votes: Leader(dice)→#5, P2(dice)→#12, P3(dice)→#18")
    print(f"Result: Character #{result_4}")
    
    if result_4 == 5:
        results.add_pass("Leader's dice vote wins when all different")
    else:
        results.add_fail("Leader dice", f"Expected 5, got {result_4}")
    
    # Test 5: Two dice votes land on same character (majority)
    print("\n📋 Test 5: Two dice votes → Same character (lucky!)")
    print("-" * 70)
    votes_5 = {
        1001: 25,  # Leader dice → Character 25
        1002: 25,  # Player 2 dice → Character 25 (same!)
        1003: 40   # Player 3 manual → Character 40
    }
    
    result_5 = voting_handler.resolve_team_vote(votes_5, team_players)
    print(f"Votes: Leader(dice)→#25, P2(dice)→#25, P3(manual)→#40")
    print(f"Result: Character #{result_5}")
    
    if result_5 == 25:
        results.add_pass("Dice votes can form majority (2 same)")
    else:
        results.add_fail("Dice majority", f"Expected 25, got {result_5}")
    
    # Test 6: Non-leader uses dice, leader uses manual
    print("\n📋 Test 6: Non-leader dice, Leader manual, all different")
    print("-" * 70)
    votes_6 = {
        1001: 7,   # Leader manual → Character 7
        1002: 33,  # Player 2 dice → Character 33
        1003: 44   # Player 3 manual → Character 44
    }
    
    result_6 = voting_handler.resolve_team_vote(votes_6, team_players)
    print(f"Votes: Leader(manual)→#7, P2(dice)→#33, P3(manual)→#44")
    print(f"Result: Character #{result_6}")
    
    if result_6 == 7:
        results.add_pass("Leader manual beats non-leader dice")
    else:
        results.add_fail("Leader vs dice", f"Expected 7, got {result_6}")
    
    # Test 7: One dice vote joins manual vote (majority)
    print("\n📋 Test 7: Dice vote + Manual vote → Same character")
    print("-" * 70)
    votes_7 = {
        1001: 9,   # Leader manual → Character 9
        1002: 16,  # Player 2 dice → Character 16
        1003: 16   # Player 3 manual → Character 16 (matches dice!)
    }
    
    result_7 = voting_handler.resolve_team_vote(votes_7, team_players)
    print(f"Votes: Leader(manual)→#9, P2(dice)→#16, P3(manual)→#16")
    print(f"Result: Character #{result_7}")
    
    if result_7 == 16:
        results.add_pass("Dice + Manual can form majority")
    else:
        results.add_fail("Dice + Manual majority", f"Expected 16, got {result_7}")
    
    # Test 8: Empty votes
    print("\n📋 Test 8: No votes - Returns None")
    print("-" * 70)
    votes_8 = {}
    
    result_8 = voting_handler.resolve_team_vote(votes_8, team_players)
    print(f"Votes: (none)")
    print(f"Result: {result_8}")
    
    if result_8 is None:
        results.add_pass("Empty votes return None")
    else:
        results.add_fail("Empty votes", f"Expected None, got {result_8}")


async def test_vote_counting_logic():
    """Test the vote counting mechanism"""
    print("\n📊 Test: Vote Counting Logic")
    print("="*70)
    
    team_players = [
        {'user_id': 2001, 'username': 'Alice', 'is_leader': True},
        {'user_id': 2002, 'username': 'Bob', 'is_leader': False},
        {'user_id': 2003, 'username': 'Charlie', 'is_leader': False}
    ]
    
    # Test unanimous vote
    print("\n📋 Test: Unanimous vote (all same)")
    print("-" * 70)
    votes = {
        2001: 100,
        2002: 100,
        2003: 100
    }
    
    result = voting_handler.resolve_team_vote(votes, team_players)
    print(f"Votes: All→#100")
    print(f"Result: Character #{result}")
    
    if result == 100:
        results.add_pass("Unanimous vote works")
    else:
        results.add_fail("Unanimous vote", f"Expected 100, got {result}")
    
    # Test partial voting (only 2 players voted)
    print("\n📋 Test: Partial voting (2 out of 3)")
    print("-" * 70)
    votes = {
        2001: 50,  # Leader voted
        2002: 60   # Player 2 voted
        # Player 3 didn't vote
    }
    
    result = voting_handler.resolve_team_vote(votes, team_players)
    print(f"Votes: Leader→#50, P2→#60, P3→(no vote)")
    print(f"Result: Character #{result}")
    
    if result == 50:
        results.add_pass("Partial voting - Leader wins")
    else:
        results.add_fail("Partial voting", f"Expected 50, got {result}")


async def main():
    """Run all dice voting tests"""
    print("="*70)
    print("🎲 DICE VOTING + TEAM RESOLUTION TEST SUITE")
    print("="*70)
    print("\nTesting dice votes work with team majority voting...\n")
    
    try:
        # Connect to database (needed for character lookups)
        await db_manager.create_pool()
        await db_manager.init_database()
        
        # Run tests
        await test_dice_vote_resolution()
        await test_vote_counting_logic()
        
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

