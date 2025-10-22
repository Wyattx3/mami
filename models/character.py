"""
Character model
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Character:
    """Character data model"""
    id: Optional[int]
    name: str
    mbti: str
    zodiac: str
    description: str
    personality_traits: Optional[str] = None
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'mbti': self.mbti,
            'zodiac': self.zodiac,
            'description': self.description,
            'personality_traits': self.personality_traits
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary"""
        return cls(
            id=data.get('id'),
            name=data['name'],
            mbti=data['mbti'],
            zodiac=data['zodiac'],
            description=data['description'],
            personality_traits=data.get('personality_traits')
        )



