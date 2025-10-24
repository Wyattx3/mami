"""
Scoring service for game results
"""
from typing import Dict, List, Any, Tuple
import logging
from database.db_manager import db_manager
from utils.helpers import get_team_name
from data.themes import get_theme_by_id

# Setup logger
logger = logging.getLogger(__name__)

# Pre-defined MBTI scores for each role (1-10)
MBTI_SCORES = {
    'ဘုရင်': {  # Leader
        'ENTJ': 10, 'ESTJ': 10, 'ENFJ': 9, 'ENTP': 8,
        'ESFJ': 7, 'ESTP': 7, 'INTJ': 6, 'ISTJ': 6,
        'INTP': 5, 'INFJ': 5, 'ISTP': 4, 'ISFJ': 4,
        'ENFP': 3, 'ESFP': 3, 'INFP': 2, 'ISFP': 2
    },
    'စစ်သူကြီး': {  # Brave/Warrior
        'ESTP': 10, 'ENTP': 9, 'ISTP': 9, 'ENTJ': 8,
        'ESTJ': 8, 'INTP': 7, 'ESFP': 7, 'ENFP': 6,
        'INTJ': 5, 'ENFJ': 5, 'ISTJ': 4, 'ESFJ': 4,
        'INFJ': 3, 'ISFP': 3, 'INFP': 2, 'ISFJ': 2
    },
    'အကြံပေး': {  # Wise/Advisor
        'INTJ': 10, 'INTP': 10, 'INFJ': 9, 'ENTJ': 8,
        'ENTP': 8, 'ESTJ': 10, 'ISTJ': 7, 'INFP': 7,
        'ENFJ': 6, 'ISTP': 5, 'ENFP': 5, 'ISFJ': 4,
        'ESFJ': 3, 'ISFP': 3, 'ESTP': 2, 'ESFP': 2
    },
    'လယ်သမား': {  # Business-minded/Farmer
        'ESTJ': 10, 'ENTJ': 10, 'ISTJ': 9, 'ESTP': 8,
        'ISTP': 8, 'INTJ': 7, 'ESFJ': 7, 'ENTP': 6,
        'INTP': 5, 'ENFJ': 5, 'ISFJ': 4, 'ESFP': 4,
        'ENFP': 3, 'INFJ': 3, 'INFP': 2, 'ISFP': 2
    },
    'ဘုန်းကြီး': {  # Polite/Diplomatic/Monk
        'ENFJ': 10, 'INFJ': 10, 'ESFJ': 9, 'ENFP': 8,
        'ISFJ': 8, 'INFP': 7, 'ENTJ': 6, 'INTJ': 6,
        'ENTP': 5, 'INTP': 5, 'ESFP': 4, 'ISFP': 4,
        'ESTJ': 3, 'ISTJ': 3, 'ESTP': 2, 'ISTP': 2
    }
}

# Pre-defined Zodiac scores for each role (1-10)
ZODIAC_SCORES = {
    'ဘုရင်': {  # Leader
        'Leo': 10, 'Aries': 10, 'Capricorn': 9, 'Scorpio': 8,
        'Sagittarius': 7, 'Aquarius': 7, 'Gemini': 6, 'Taurus': 6,
        'Virgo': 5, 'Libra': 5, 'Cancer': 3, 'Pisces': 2
    },
    'စစ်သူကြီး': {  # Brave/Warrior
        'Aries': 10, 'Scorpio': 10, 'Leo': 9, 'Sagittarius': 8,
        'Capricorn': 7, 'Gemini': 7, 'Aquarius': 6, 'Taurus': 6,
        'Virgo': 5, 'Cancer': 4, 'Libra': 3, 'Pisces': 2
    },
    'အကြံပေး': {  # Wise/Advisor
        'Virgo': 10, 'Aquarius': 10, 'Capricorn': 9, 'Scorpio': 8,
        'Gemini': 8, 'Libra': 7, 'Pisces': 7, 'Cancer': 6,
        'Taurus': 5, 'Leo': 4, 'Sagittarius': 3, 'Aries': 2
    },
    'လယ်သမား': {  # Business-minded/Farmer
        'Capricorn': 10, 'Taurus': 10, 'Virgo': 9, 'Scorpio': 8,
        'Leo': 7, 'Aries': 7, 'Gemini': 6, 'Aquarius': 6,
        'Sagittarius': 5, 'Cancer': 4, 'Libra': 3, 'Pisces': 2
    },
    'ဘုန်းကြီး': {  # Polite/Diplomatic/Monk
        'Libra': 10, 'Pisces': 10, 'Cancer': 9, 'Taurus': 8,
        'Virgo': 7, 'Aquarius': 7, 'Gemini': 6, 'Capricorn': 6,
        'Sagittarius': 5, 'Scorpio': 4, 'Leo': 3, 'Aries': 2
    }
}


class ScoringService:
    """Handles game scoring and results calculation"""
    
    def calculate_character_score(self, character, role_name: str) -> Tuple[int, str]:
        """Calculate score based on pre-defined MBTI and Zodiac scores
        
        Args:
            character: Character object with mbti and zodiac
            role_name: Role name (e.g., ဘုရင်)
            
        Returns:
            Tuple of (score: 1-10, explanation: str)
        """
        logger.debug(f"Calculating score for {character.name} - Role: {role_name}")
        
        # Get MBTI score
        mbti_score_dict = MBTI_SCORES.get(role_name, {})
        mbti_score = mbti_score_dict.get(character.mbti, 5)  # Default 5 if not found
        
        # Get Zodiac score
        zodiac_score_dict = ZODIAC_SCORES.get(role_name, {})
        zodiac_score = zodiac_score_dict.get(character.zodiac, 5)  # Default 5 if not found
        
        # Calculate average score (weighted: 60% MBTI, 40% Zodiac)
        final_score = int((mbti_score * 0.6) + (zodiac_score * 0.4))
        final_score = max(1, min(10, final_score))  # Ensure 1-10 range
        
        # Generate explanation
        explanation = self._generate_explanation(
            character.name, character.mbti, character.zodiac,
            role_name, mbti_score, zodiac_score, final_score
        )
        
        logger.info(f"Score calculated: {character.name} for {role_name} = {final_score}/10")
        return final_score, explanation
    
    def _generate_explanation(self, char_name: str, mbti: str, zodiac: str,
                             role: str, mbti_score: int, zodiac_score: int,
                             final_score: int) -> str:
        """Generate explanation for the score"""
        
        # Score level descriptions
        if final_score >= 9:
            level = "အလွန်လိုက်ဖက်"
        elif final_score >= 7:
            level = "သင့်တော်"
        elif final_score >= 5:
            level = "အလယ်အလတ်"
        elif final_score >= 3:
            level = "သင့်လျော်မှု နည်း"
        else:
            level = "မလိုက်ဖက်"
        
        explanation = f"""
**{char_name}** သည် **{role}** အခန်းကဏ္ဍအတွက် **{level}** ဖြစ်ပါသည်။

📊 **Score Breakdown:**
• MBTI ({mbti}): {mbti_score}/10
• Zodiac ({zodiac}): {zodiac_score}/10
• **Final Score: {final_score}/10**

{self._get_role_description(role, mbti, zodiac, final_score)}
"""
        return explanation.strip()
    
    def _get_role_description(self, role: str, mbti: str, zodiac: str, score: int) -> str:
        """Get specific description for role-character match"""
        
        descriptions = {
            'ဘုရင်': {
                'high': f"{mbti} သည် ဦးဆောင်မှုရှိပြီး {zodiac} က ခေါင်းဆောင်စွမ်းရည် ကောင်းမွန်ပါသည်။",
                'medium': f"{mbti} နဲ့ {zodiac} တို့က ဦးဆောင်နိုင်စွမ်း အတန်အသင့် ရှိပါသည်။",
                'low': f"{mbti} နဲ့ {zodiac} တို့သည် ဦးဆောင်မှုထက် အခြားနယ်ပယ်များတွင် ပိုသင့်တော်ပါသည်။"
            },
            'စစ်သူကြီး': {
                'high': f"{mbti} က စွန့်ဦးတင်းမာမှု ရှိပြီး {zodiac} သည် သတ္တိ ပြည့်ဝပါသည်။",
                'medium': f"{mbti} နဲ့ {zodiac} တို့မှာ သတ္တိရှိမှု အတန်အသင့် ပါဝင်ပါသည်။",
                'low': f"{mbti} နဲ့ {zodiac} တို့သည် တိုက်ပွဲထက် စီမံခန့်ခွဲရေးတွင် ပိုသင့်တော်ပါသည်။"
            },
            'အကြံပေး': {
                'high': f"{mbti} သည် ဉာဏ်ရည်မြင့်ပြီး {zodiac} က ဉာဏ်ပညာရှိ အကြံပေးနိုင်ပါသည်။",
                'medium': f"{mbti} နဲ့ {zodiac} တို့က အကြံပေးနိုင်စွမ်း အတန်အသင့် ရှိပါသည်။",
                'low': f"{mbti} နဲ့ {zodiac} တို့သည် လက်တွေ့ကျတဲ့ အလုပ်များတွင် ပိုသင့်တော်ပါသည်။"
            },
            'လယ်သမား': {
                'high': f"{mbti} က စီးပွားရေးအာရုံ ကောင်းမွန်ပြီး {zodiac} သည် လက်တွေ့ကျပါသည်။",
                'medium': f"{mbti} နဲ့ {zodiac} တို့မှာ စီးပွားရေးစွမ်းရည် အတန်အသင့် ရှိပါသည်။",
                'low': f"{mbti} နဲ့ {zodiac} တို့သည် ဖန်တီးမှုနယ်ပယ်များတွင် ပိုသင့်တော်ပါသည်။"
            },
            'ဘုန်းကြီး': {
                'high': f"{mbti} သည် စာနာတတ်ပြီး {zodiac} က လိမ္မာယဥ်ကျေးပါသည်။",
                'medium': f"{mbti} နဲ့ {zodiac} တို့မှာ ယဉ်ကျေးမှု အတန်အသင့် ရှိပါသည်။",
                'low': f"{mbti} နဲ့ {zodiac} တို့သည် တိုက်ရိုက်ပြောဆိုရတဲ့ အလုပ်များတွင် ပိုသင့်တော်ပါသည်။"
            }
        }
        
        role_desc = descriptions.get(role, {})
        if score >= 7:
            return role_desc.get('high', '')
        elif score >= 4:
            return role_desc.get('medium', '')
        else:
            return role_desc.get('low', '')
    
    async def score_game(self, game_id: int) -> Dict[int, Dict[str, Any]]:
        """Score all teams in a game
        
        Args:
            game_id: Game ID
            
        Returns:
            Dictionary with team scores and details
        """
        logger.info(f"Scoring game {game_id}")
        
        # Get all rounds for the game
        rounds = await db_manager.get_game_rounds(game_id)
        logger.debug(f"Game {game_id} has {len(rounds)} round entries")
        
        # Get teams
        teams = await db_manager.get_game_players(game_id)
        
        # Score each team
        team_scores = {}
        for team_id in teams.keys():
            logger.debug(f"Scoring team {team_id}")
            team_rounds = [r for r in rounds if r.team_id == team_id]
            
            # Score each round
            for game_round in team_rounds:
                if game_round.selected_character_id:
                    character = await db_manager.get_character(game_round.selected_character_id)
                    
                    if character:
                        # Get role info from theme
                        theme_id = await db_manager.get_game_theme(game_id)
                        theme = get_theme_by_id(theme_id)
                        role_info = theme['roles'].get(game_round.round_number, {})
                        role_name = role_info.get('name', '')
                        
                        # Calculate score using pre-defined system
                        score, explanation = self.calculate_character_score(
                            character, role_name
                        )
                        
                        # Save score
                        logger.debug(f"Team {team_id} - Round {game_round.round_number} - Score: {score}")
                        await db_manager.save_round_score(
                            game_id, game_round.round_number, team_id, score, explanation
                        )
        
        # Get final results
        results = await db_manager.get_game_results(game_id)
        
        # Add team players info
        for team_id in results.keys():
            results[team_id]['players'] = teams.get(team_id, [])
        
        logger.info(f"Game {game_id} scoring completed")
        for team_id, data in results.items():
            logger.info(f"Team {team_id}: {data['total_score']} points")
        
        return results
    
    def determine_winner(self, results: Dict[int, Dict[str, Any]]) -> int:
        """Determine winning team
        
        Args:
            results: Team results with scores
            
        Returns:
            Winning team number
        """
        max_score = -1
        winner = 1
        
        for team_id, data in results.items():
            total_score = data.get('total_score', 0)
            if total_score > max_score:
                max_score = total_score
                winner = team_id
        
        logger.info(f"Winner determined: Team {winner} with {max_score} points")
        return winner
    
    def format_team_results(self, team_id: int, results: Dict[str, Any]) -> str:
        """Format results for a single team
        
        Args:
            team_id: Team number
            results: Team results data
            
        Returns:
            Formatted message
        """
        # Get team name from players
        players = results.get('players', [])
        team_name = get_team_name(players) if players else f"Team {team_id}"
        
        lines = [f"🏆 **{team_name} Results**\n"]
        
        # Players
        if players:
            player_names = ', '.join([f"@{p['username']}" for p in players])
            lines.append(f"**Players:** {player_names}")
        
        lines.append("━━━━━━━━━━")
        
        # Rounds
        rounds = results.get('rounds', [])
        for round_data in rounds:
            role = round_data.get('role', '')
            char_name = round_data.get('character_name', 'Optional')
            score = round_data.get('score', 0)
            lines.append(f"{role}: {char_name} ({score} မှတ်)")
        
        lines.append("")
        lines.append(f"**Total: {results.get('total_score', 0)} မှတ်**")
        
        return "\n".join(lines)
    
    def format_all_results(self, results: Dict[int, Dict[str, Any]], 
                          winner_team: int) -> List[str]:
        """Format results for all teams
        
        Args:
            results: All team results
            winner_team: Winning team number
            
        Returns:
            List of formatted messages (one per team)
        """
        messages = []
        
        for team_id in sorted(results.keys()):
            team_results = results[team_id]
            message = self.format_team_results(team_id, team_results)
            
            # Add winner indicator
            if team_id == winner_team:
                message = "👑 **WINNER!** 👑\n\n" + message
            
            messages.append(message)
        
        return messages


# Global scoring service instance
scoring_service = ScoringService()



