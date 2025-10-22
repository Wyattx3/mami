"""
Team management service
"""
from typing import Dict, List, Any
import random
import config
from utils.helpers import shuffle_players, split_into_teams, format_team_announcement


class TeamService:
    """Handles team formation and management"""
    
    def __init__(self):
        self.team_size = config.TEAM_SIZE
        self.num_teams = config.NUM_TEAMS
    
    def form_teams(self, players: List[Dict[str, Any]]) -> Dict[int, List[Dict[str, Any]]]:
        """Form random teams from players and assign leaders
        
        Args:
            players: List of player dicts with user_id and username
            
        Returns:
            Dictionary mapping team_number to list of players (with is_leader field)
        """
        if len(players) != config.LOBBY_SIZE:
            raise ValueError(f"Need exactly {config.LOBBY_SIZE} players, got {len(players)}")
        
        teams = split_into_teams(players, self.team_size)
        
        # Assign random leader to each team
        for team_num, team_players in teams.items():
            # Pick random leader
            leader_index = random.randint(0, len(team_players) - 1)
            
            # Mark leader
            for i, player in enumerate(team_players):
                player['is_leader'] = (i == leader_index)
        
        return teams
    
    def get_team_announcement_message(self, teams: Dict[int, List[Dict[str, Any]]]) -> str:
        """Get formatted team announcement message"""
        return format_team_announcement(teams)
    
    def flatten_teams_for_db(self, teams: Dict[int, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Flatten teams structure for database storage
        
        Args:
            teams: Dict mapping team_number to players
            
        Returns:
            List of players with team_number and is_leader added
        """
        flattened = []
        for team_num, players in teams.items():
            for player in players:
                flattened.append({
                    'user_id': player['user_id'],
                    'username': player['username'],
                    'team_number': team_num,
                    'is_leader': player.get('is_leader', False)
                })
        return flattened
    
    def get_team_player_ids(self, teams: Dict[int, List[Dict[str, Any]]], 
                           team_number: int) -> List[int]:
        """Get user IDs for a specific team
        
        Args:
            teams: Teams dictionary
            team_number: Team number (1-3)
            
        Returns:
            List of user IDs
        """
        if team_number not in teams:
            return []
        
        return [player['user_id'] for player in teams[team_number]]


# Global team service instance
team_service = TeamService()



