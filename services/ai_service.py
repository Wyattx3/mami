"""
AI Service for Gemini integration
"""
import google.generativeai as genai
import re
import logging
from typing import Tuple, Optional
import config
from models.character import Character

# Setup logger
logger = logging.getLogger(__name__)


class AIService:
    """Handles all AI-related operations using Gemini"""
    
    def __init__(self):
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def generate_character_description(self, character: Character) -> str:
        """Generate character description for voting display
        
        Args:
            character: Character object
            
        Returns:
            Description in Burmese
        """
        logger.debug(f"Generating AI description for character: {character.name}")
        prompt = f"""
ဒီ character {character.name} က {character.mbti} MBTI နှင့် {character.zodiac} zodiac ပါတယ်။ 
သူ့ရဲ့ ပုဂ္ဂိုလ်ရေး ဝိသေသလက္ခဏာတွေကို မြန်မာလို 2-3 စာကြောင်းနှင့် ရှင်းပြပေးပါ။
သူက ဘယ်လို လူမျိုးလဲ၊ သူ့ရဲ့ အားသာချက်တွေက ဘာတွေလဲ။
"""
        
        try:
            response = self.model.generate_content(prompt)
            description = response.text.strip()
            logger.info(f"AI description generated for {character.name}: {len(description)} chars")
            return description
        except Exception as e:
            logger.error(f"AI Error generating description: {e}")
            # Fallback description
            fallback = f"{character.name} သည် {character.mbti} လူမျိုးဖြစ်ပြီး {character.zodiac} နဲ့ မွေးဖွားသူဖြစ်ပါတယ်။"
            logger.warning(f"Using fallback description for {character.name}")
            return fallback
    
    async def score_character_role_match(self, character: Character, role: str, 
                                        role_description: str) -> Tuple[int, str]:
        """Score how well a character matches a role
        
        Args:
            character: Character object
            role: Role name (e.g., ဘုရင်)
            role_description: Role description (e.g., ဦးဆောင်နိုင်တဲ့သူ)
            
        Returns:
            Tuple of (score: 0-10, explanation: str)
        """
        logger.debug(f"Scoring character-role match: {character.name} for {role}")
        prompt = f"""
Character: {character.name}
MBTI: {character.mbti}
Zodiac: {character.zodiac}

Role: {role} ({role_description})

ဒီ character က ဒီ role အတွက် ဘယ်လောက်လိုက်ဖက်လဲ? 

1-10 အတွင်း score ပေးပြီး အကြောင်းပြချက် 3-4 စာကြောင်းနဲ့ မြန်မာလို ရှင်းပြပါ။
MBTI နှင့် Zodiac sign တို့ရဲ့ လက္ခဏာတွေကို အခြေခံပြီး ရှင်းပြပါ။

Format:
Score: [1-10 ကြား ဂဏန်း]
Explanation: [အကြောင်းပြချက်]
"""
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Parse score
            score_match = re.search(r'Score:\s*(\d+)', text)
            if score_match:
                score = int(score_match.group(1))
                score = max(1, min(10, score))  # Ensure 1-10
            else:
                # Try to find any number in the response
                numbers = re.findall(r'\b(\d+)\b', text)
                if numbers:
                    score = int(numbers[0])
                    score = max(1, min(10, score))
                else:
                    score = 5  # Default middle score
            
            # Parse explanation
            explanation_match = re.search(r'Explanation:\s*(.+)', text, re.DOTALL)
            if explanation_match:
                explanation = explanation_match.group(1).strip()
            else:
                # Use the whole response as explanation
                explanation = text
            
            logger.info(f"AI scored {character.name} for {role}: {score}/10")
            return score, explanation
            
        except Exception as e:
            logger.error(f"AI Scoring Error: {e}")
            # Fallback scoring
            fallback_score = 5
            fallback_explanation = f"{character.name} သည် {role} အခန်းကဏ္ဍအတွက် အလယ်အလတ် သင့်တော်ပါသည်။"
            logger.warning(f"Using fallback score for {character.name}: {fallback_score}/10")
            return fallback_score, fallback_explanation
    
    async def batch_score_team_selections(self, game_id: int, team_rounds: list) -> list:
        """Score all character-role selections for a team
        
        Args:
            game_id: Game ID
            team_rounds: List of round data with character and role info
            
        Returns:
            List of scored rounds
        """
        scored_rounds = []
        
        for round_data in team_rounds:
            character = round_data.get('character')
            role = round_data.get('role')
            role_description = round_data.get('role_description')
            
            if character and role:
                score, explanation = await self.score_character_role_match(
                    character, role, role_description
                )
                scored_rounds.append({
                    'round_number': round_data['round_number'],
                    'role': role,
                    'character': character,
                    'score': score,
                    'explanation': explanation
                })
        
        return scored_rounds


# Global AI service instance
ai_service = AIService()



