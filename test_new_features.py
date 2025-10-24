"""
Comprehensive Test Suite for New Game Features
Tests all recent changes and improvements
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

import config
from database.db_manager import db_manager
from services.team_service import team_service
from utils.helpers import parse_vote_callback


class TestResults:
    """Track test results"""
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
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {self.total}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"Success Rate: {(self.passed/self.total)*100:.1f}%")
        
        if self.errors:
            print("\n❌ Failed Tests:")
            for test_name, reason in self.errors:
                print(f"  - {test_name}: {reason}")
        
        print("="*60)


results = TestResults()


async def test_config_updates():
    """Test 1: Config Updates"""
    print("\n🔧 Test 1: Configuration Updates")
    print("-" * 60)
    
    # Test MIN_PLAYERS
    if config.MIN_PLAYERS == 6:
        results.add_pass("MIN_PLAYERS = 6")
    else:
        results.add_fail("MIN_PLAYERS", f"Expected 6, got {config.MIN_PLAYERS}")
    
    # Test MAX_PLAYERS
    if config.MAX_PLAYERS == 15:
        results.add_pass("MAX_PLAYERS = 15")
    else:
        results.add_fail("MAX_PLAYERS", f"Expected 15, got {config.MAX_PLAYERS}")
    
    # Test TEAM_SIZE
    if config.TEAM_SIZE == 3:
        results.add_pass("TEAM_SIZE = 3")
    else:
        results.add_fail("TEAM_SIZE", f"Expected 3, got {config.TEAM_SIZE}")
    
    # Test LOBBY_TIMEOUT
    if config.LOBBY_TIMEOUT == 60:
        results.add_pass("LOBBY_TIMEOUT = 60")
    else:
        results.add_fail("LOBBY_TIMEOUT", f"Expected 60, got {config.LOBBY_TIMEOUT}")
    
    # Test CHARACTERS_PER_VOTING
    if config.CHARACTERS_PER_VOTING == 5:
        results.add_pass("CHARACTERS_PER_VOTING = 5")
    else:
        results.add_fail("CHARACTERS_PER_VOTING", f"Expected 5, got {config.CHARACTERS_PER_VOTING}")


async def test_database_connection():
    """Test 2: Database Connection"""
    print("\n🗄️ Test 2: Database Connection")
    print("-" * 60)
    
    try:
        await db_manager.create_pool()
        results.add_pass("Database connection pool created")
        
        await db_manager.init_database()
        results.add_pass("Database initialized")
        
        # Test character count
        char_count = await db_manager.get_character_count()
        if char_count >= 15:  # Need at least 15 for 3 rounds
            results.add_pass(f"Character database ready ({char_count} characters)")
        else:
            results.add_fail("Character database", f"Only {char_count} characters, need at least 15")
        
    except Exception as e:
        results.add_fail("Database connection", str(e))


async def test_dice_voting_callback():
    """Test 3: Dice Voting Callback Parsing"""
    print("\n🎲 Test 3: Dice Voting Callback")
    print("-" * 60)
    
    # Test normal character callback
    normal_callback = "vote_1_2_3_45"
    result = parse_vote_callback(normal_callback)
    
    if result and result['character_id'] == 45:
        results.add_pass("Normal character callback parsing")
    else:
        results.add_fail("Normal character callback", f"Got {result}")
    
    # Test dice callback
    dice_callback = "vote_1_2_3_dice"
    result = parse_vote_callback(dice_callback)
    
    if result and result['character_id'] == 'dice':
        results.add_pass("Dice callback parsing")
    else:
        results.add_fail("Dice callback", f"Got {result}")
    
    # Test invalid callback
    invalid_callback = "vote_invalid"
    result = parse_vote_callback(invalid_callback)
    
    if result is None:
        results.add_pass("Invalid callback rejection")
    else:
        results.add_fail("Invalid callback", "Should return None")


async def test_team_formation():
    """Test 4: Dynamic Team Formation"""
    print("\n🏆 Test 4: Dynamic Team Formation")
    print("-" * 60)
    
    # Test 6 players (2 teams)
    players_6 = [
        {'user_id': i, 'username': f'Player{i}'}
        for i in range(1, 7)
    ]
    
    try:
        teams = team_service.form_teams(players_6)
        if len(teams) == 2 and all(len(team) == 3 for team in teams.values()):
            results.add_pass("6 players → 2 teams of 3")
        else:
            results.add_fail("6 players", f"Got {len(teams)} teams")
    except Exception as e:
        results.add_fail("6 players team formation", str(e))
    
    # Test 9 players (3 teams)
    players_9 = [
        {'user_id': i, 'username': f'Player{i}'}
        for i in range(1, 10)
    ]
    
    try:
        teams = team_service.form_teams(players_9)
        if len(teams) == 3 and all(len(team) == 3 for team in teams.values()):
            results.add_pass("9 players → 3 teams of 3")
        else:
            results.add_fail("9 players", f"Got {len(teams)} teams")
    except Exception as e:
        results.add_fail("9 players team formation", str(e))
    
    # Test 12 players (4 teams)
    players_12 = [
        {'user_id': i, 'username': f'Player{i}'}
        for i in range(1, 13)
    ]
    
    try:
        teams = team_service.form_teams(players_12)
        if len(teams) == 4 and all(len(team) == 3 for team in teams.values()):
            results.add_pass("12 players → 4 teams of 3")
        else:
            results.add_fail("12 players", f"Got {len(teams)} teams")
    except Exception as e:
        results.add_fail("12 players team formation", str(e))
    
    # Test 15 players (5 teams)
    players_15 = [
        {'user_id': i, 'username': f'Player{i}'}
        for i in range(1, 16)
    ]
    
    try:
        teams = team_service.form_teams(players_15)
        if len(teams) == 5 and all(len(team) == 3 for team in teams.values()):
            results.add_pass("15 players → 5 teams of 3")
        else:
            results.add_fail("15 players", f"Got {len(teams)} teams")
    except Exception as e:
        results.add_fail("15 players team formation", str(e))
    
    # Test invalid player count (should fail)
    players_7 = [
        {'user_id': i, 'username': f'Player{i}'}
        for i in range(1, 8)
    ]
    
    try:
        teams = team_service.form_teams(players_7)
        results.add_fail("7 players validation", "Should raise ValueError")
    except ValueError as e:
        results.add_pass("7 players validation (correctly rejected)")
    except Exception as e:
        results.add_fail("7 players validation", f"Wrong exception: {e}")
    
    # Test minimum players
    players_5 = [
        {'user_id': i, 'username': f'Player{i}'}
        for i in range(1, 6)
    ]
    
    try:
        teams = team_service.form_teams(players_5)
        results.add_fail("5 players validation", "Should raise ValueError")
    except ValueError as e:
        results.add_pass("Minimum players validation (correctly rejected)")
    except Exception as e:
        results.add_fail("Minimum players validation", f"Wrong exception: {e}")


async def test_lobby_operations():
    """Test 5: Lobby Operations"""
    print("\n🎮 Test 5: Lobby Operations")
    print("-" * 60)
    
    try:
        # Clear lobby first
        await db_manager.clear_lobby()
        results.add_pass("Lobby cleared")
        
        # Test adding players
        added = await db_manager.add_to_lobby(12345, "TestPlayer1")
        if added:
            results.add_pass("Add player to lobby")
        else:
            results.add_fail("Add player", "Failed to add")
        
        # Test lobby count
        count = await db_manager.get_lobby_count()
        if count == 1:
            results.add_pass("Lobby count tracking")
        else:
            results.add_fail("Lobby count", f"Expected 1, got {count}")
        
        # Test duplicate prevention
        added = await db_manager.add_to_lobby(12345, "TestPlayer1")
        if not added:
            results.add_pass("Duplicate player prevention")
        else:
            results.add_fail("Duplicate prevention", "Allowed duplicate")
        
        # Test get lobby players
        players = await db_manager.get_lobby_players()
        if len(players) == 1 and players[0]['user_id'] == 12345:
            results.add_pass("Get lobby players")
        else:
            results.add_fail("Get lobby players", f"Got {len(players)} players")
        
        # Test remove player
        removed = await db_manager.remove_from_lobby(12345)
        if removed:
            results.add_pass("Remove player from lobby")
        else:
            results.add_fail("Remove player", "Failed to remove")
        
        # Verify empty
        count = await db_manager.get_lobby_count()
        if count == 0:
            results.add_pass("Lobby empty after removal")
        else:
            results.add_fail("Lobby empty", f"Still has {count} players")
        
        # Clean up
        await db_manager.clear_lobby()
        
    except Exception as e:
        results.add_fail("Lobby operations", str(e))


async def test_lobby_handler():
    """Test 6: Lobby Handler Features"""
    print("\n⏱️ Test 6: Lobby Handler Features")
    print("-" * 60)
    
    from handlers.lobby_handler import lobby_handler
    
    # Test timer attributes
    if hasattr(lobby_handler, 'lobby_timeout'):
        if lobby_handler.lobby_timeout == 60:
            results.add_pass("Lobby handler timeout configured")
        else:
            results.add_fail("Lobby timeout", f"Expected 60, got {lobby_handler.lobby_timeout}")
    else:
        results.add_fail("Lobby handler", "Missing lobby_timeout attribute")
    
    # Test min/max players
    if hasattr(lobby_handler, 'min_players') and hasattr(lobby_handler, 'max_players'):
        if lobby_handler.min_players == 6 and lobby_handler.max_players == 15:
            results.add_pass("Lobby handler player limits")
        else:
            results.add_fail("Player limits", f"Min: {lobby_handler.min_players}, Max: {lobby_handler.max_players}")
    else:
        results.add_fail("Lobby handler", "Missing player limit attributes")
    
    # Test timer methods
    if hasattr(lobby_handler, 'start_lobby_timer'):
        results.add_pass("Lobby timer start method exists")
    else:
        results.add_fail("Lobby timer", "Missing start_lobby_timer method")
    
    if hasattr(lobby_handler, 'cancel_lobby_timer'):
        results.add_pass("Lobby timer cancel method exists")
    else:
        results.add_fail("Lobby timer", "Missing cancel_lobby_timer method")


async def test_voting_handler():
    """Test 7: Voting Handler Features"""
    print("\n🗳️ Test 7: Voting Handler Features")
    print("-" * 60)
    
    from handlers.voting_handler import voting_handler
    
    # Test voting handler exists
    if voting_handler:
        results.add_pass("Voting handler initialized")
    else:
        results.add_fail("Voting handler", "Not initialized")
    
    # Test methods exist
    if hasattr(voting_handler, 'create_voting_keyboard'):
        results.add_pass("Create voting keyboard method exists")
    else:
        results.add_fail("Voting keyboard", "Missing method")
    
    if hasattr(voting_handler, 'handle_vote'):
        results.add_pass("Handle vote method exists")
    else:
        results.add_fail("Handle vote", "Missing method")


async def test_game_flow_validation():
    """Test 8: Game Flow Validation"""
    print("\n🎯 Test 8: Game Flow Validation")
    print("-" * 60)
    
    # Test player count scenarios
    valid_counts = [6, 9, 12, 15]
    invalid_counts = [5, 7, 8, 10, 11, 13, 14, 16]
    
    for count in valid_counts:
        if count % config.TEAM_SIZE == 0 and config.MIN_PLAYERS <= count <= config.MAX_PLAYERS:
            results.add_pass(f"{count} players is valid")
        else:
            results.add_fail(f"{count} players", "Should be valid")
    
    for count in invalid_counts:
        if count % config.TEAM_SIZE != 0 or count < config.MIN_PLAYERS or count > config.MAX_PLAYERS:
            results.add_pass(f"{count} players is invalid (correctly)")
        else:
            results.add_fail(f"{count} players", "Should be invalid")


async def main():
    """Run all tests"""
    print("="*60)
    print("🧪 COMPREHENSIVE FEATURE TEST SUITE")
    print("="*60)
    print("\nTesting all recent changes and improvements...")
    
    try:
        # Run all tests
        await test_config_updates()
        await test_database_connection()
        await test_dice_voting_callback()
        await test_team_formation()
        await test_lobby_operations()
        await test_lobby_handler()
        await test_voting_handler()
        await test_game_flow_validation()
        
        # Show summary
        results.summary()
        
        # Clean up
        if db_manager.pool:
            await db_manager.close_pool()
            print("\n✅ Database connection closed")
        
        # Return exit code
        return 0 if results.failed == 0 else 1
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

