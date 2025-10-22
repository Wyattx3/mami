"""
Game model
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any
from datetime import datetime


@dataclass
class Game:
    """Game data model"""
    id: Optional[int]
    status: str
    created_at: datetime
    winner_team: Optional[int] = None
    current_round: int = 0
    lobby_message_id: Optional[int] = None
    lobby_chat_id: Optional[int] = None
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'winner_team': self.winner_team,
            'current_round': self.current_round,
            'lobby_message_id': self.lobby_message_id,
            'lobby_chat_id': self.lobby_chat_id
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary"""
        created_at = data['created_at']
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        
        return cls(
            id=data.get('id'),
            status=data['status'],
            created_at=created_at,
            winner_team=data.get('winner_team'),
            current_round=data.get('current_round', 0),
            lobby_message_id=data.get('lobby_message_id'),
            lobby_chat_id=data.get('lobby_chat_id')
        )


@dataclass
class GameRound:
    """Game round data model"""
    id: Optional[int]
    game_id: int
    round_number: int
    role: str
    team_id: int
    selected_character_id: Optional[int] = None
    votes: Optional[str] = None  # JSON string
    score: Optional[int] = None
    explanation: Optional[str] = None
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'game_id': self.game_id,
            'round_number': self.round_number,
            'role': self.role,
            'team_id': self.team_id,
            'selected_character_id': self.selected_character_id,
            'votes': self.votes,
            'score': self.score,
            'explanation': self.explanation
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary"""
        return cls(
            id=data.get('id'),
            game_id=data['game_id'],
            round_number=data['round_number'],
            role=data['role'],
            team_id=data['team_id'],
            selected_character_id=data.get('selected_character_id'),
            votes=data.get('votes'),
            score=data.get('score'),
            explanation=data.get('explanation')
        )



