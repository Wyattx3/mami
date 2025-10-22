"""
Utility helper functions
"""
import random
from typing import List, Dict, Any
from datetime import datetime


def format_player_list(players: List[Dict[str, Any]]) -> str:
    """Format player list for display"""
    if not players:
        return "No players yet"
    
    lines = []
    for i, player in enumerate(players, 1):
        username = player.get('username', 'Unknown')
        lines.append(f"{i}. @{username}")
    
    return "\n".join(lines)


def shuffle_players(players: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Randomly shuffle players"""
    shuffled = players.copy()
    random.shuffle(shuffled)
    return shuffled


def split_into_teams(players: List[Dict[str, Any]], team_size: int = 3) -> Dict[int, List[Dict[str, Any]]]:
    """Split players into teams"""
    teams = {}
    shuffled_players = shuffle_players(players)
    
    for i in range(0, len(shuffled_players), team_size):
        team_number = (i // team_size) + 1
        teams[team_number] = shuffled_players[i:i + team_size]
    
    return teams


def get_team_name(players: List[Dict[str, Any]]) -> str:
    """Get team name based on leader's username"""
    for player in players:
        if player.get('is_leader', False):
            username = player.get('username', 'Unknown')
            # Remove @ if present
            clean_name = username.lstrip('@')
            return f"Team {clean_name}"
    
    # Fallback: use first player's name
    if players:
        username = players[0].get('username', 'Unknown')
        clean_name = username.lstrip('@')
        return f"Team {clean_name}"
    
    return "Team Unknown"


def format_team_announcement(teams: Dict[int, List[Dict[str, Any]]]) -> str:
    """Format team announcement message with leaders"""
    lines = ["🎮 Team များ ခွဲခြားပြီးပါပြီ!\n"]
    
    for team_num, players in teams.items():
        team_name = get_team_name(players)
        lines.append(f"{team_name}:")
        for player in players:
            username = player.get('username', 'Unknown')
            is_leader = player.get('is_leader', False)
            
            if is_leader:
                lines.append(f"  👑 @{username} (Leader)")
            else:
                lines.append(f"  • @{username}")
        lines.append("")
    
    lines.append("Game စတင်ပါမည်... ⏳")
    return "\n".join(lines)


def format_timestamp(dt: datetime = None) -> str:
    """Format datetime to string"""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def parse_vote_callback(callback_data: str) -> Dict[str, Any]:
    """Parse vote callback data
    Format: vote_{game_id}_{round}_{team}_{character_id}
    """
    parts = callback_data.split('_')
    if len(parts) != 5 or parts[0] != 'vote':
        return None
    
    return {
        'game_id': int(parts[1]),
        'round': int(parts[2]),
        'team': int(parts[3]),
        'character_id': int(parts[4])
    }


def parse_details_callback(callback_data: str) -> Dict[str, Any]:
    """Parse details callback data
    Format: details_{game_id}_{team}_{role}
    """
    parts = callback_data.split('_')
    if len(parts) != 4 or parts[0] != 'details':
        return None
    
    return {
        'game_id': int(parts[1]),
        'team': int(parts[2]),
        'role': int(parts[3])
    }


def calculate_time_remaining(start_time: datetime, duration_seconds: int) -> int:
    """Calculate remaining seconds"""
    elapsed = (datetime.now() - start_time).total_seconds()
    remaining = max(0, duration_seconds - elapsed)
    return int(remaining)



