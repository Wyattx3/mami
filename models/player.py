"""
Player model
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Player:
    """Player data model"""
    user_id: int
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary"""
        return cls(
            user_id=data['user_id'],
            username=data.get('username', 'Unknown'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )
    
    @property
    def display_name(self) -> str:
        """Get display name"""
        if self.username:
            return f"@{self.username}"
        elif self.first_name:
            return self.first_name
        else:
            return f"User_{self.user_id}"



