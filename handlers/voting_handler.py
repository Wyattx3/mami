"""
Voting handler for character selection
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from typing import Dict, List, Any, Optional
import asyncio
import logging
from datetime import datetime
from database.db_manager import db_manager
from models.character import Character
from utils.helpers import parse_vote_callback, get_team_name
from utils.message_delivery import message_delivery
from data.themes import get_theme_by_id
import config

# Setup logger
logger = logging.getLogger(__name__)

# Pre-defined MBTI descriptions (Burmese)
MBTI_DESCRIPTIONS = {
    'INTJ': 'မဟာဗျူဟာရေးဆွဲတတ်သူ၊ အနာဂတ်ကိုကြိုမြင်သူ',
    'INTP': 'ဆင်ခြင်တုံတရားရှိသူ၊ ပြဿနာဖြေရှင်းတတ်သူ',
    'ENTJ': 'ခေါင်းဆောင်မှုကောင်းသူ၊ ရည်မှန်းချက်အောင်မြင်စေသူ',
    'ENTP': 'ဆန်းသစ်တီထွင်သူ၊ စိန်ခေါ်မှုကြိုက်သူ',
    'INFJ': 'စာနာတတ်သူ၊ အနာဂတ်ကိုစဉ်းစားသူ',
    'INFP': 'စိတ်ကူးကြွသူ၊ တန်ဖိုးမှားများကိုင်စွဲသူ',
    'ENFJ': 'လူတွေကိုလှုံ့ဆော်တတ်သူ၊ အုပ်စုဦးဆောင်သူ',
    'ENFP': 'စွမ်းအင်ပြည့်ဝသူ၊ စိတ်အားထက်သန်သူ',
    'ISTJ': 'တာဝန်သိသူ၊ ယုံကြည်စိတ်ချရသူ',
    'ISFJ': 'ဂရုစိုက်တတ်သူ၊ ကာကွယ်စောင့်ရှောက်သူ',
    'ESTJ': 'စီမံခန့်ခွဲတတ်သူ၊ စည်းကမ်းတင်းကြပ်သူ',
    'ESFJ': 'လူမှုရေးကောင်းသူ၊ ကူညီပံ့ပိုးတတ်သူ',
    'ISTP': 'လက်တွေ့ကျသူ၊ ပြဿနာဖြေရှင်းတတ်သူ',
    'ISFP': 'အနုပညာဆန်သူ၊ လွတ်လပ်စွာနေထိုင်ချင်သူ',
    'ESTP': 'စွန့်စားတတ်သူ၊ လက်တွေ့လုပ်ဆောင်သူ',
    'ESFP': 'ပျော်ရွှင်စေသူ၊ ဖျော်ဖြေတတ်သူ'
}

# Pre-defined Zodiac descriptions (Burmese)
ZODIAC_DESCRIPTIONS = {
    'Aries': 'ရဲရင့်သတ္တိရှိသူ၊ ဦးဆောင်တတ်သူ',
    'Taurus': 'တည်ငြိမ်ယုံကြည်စိတ်ချရသူ',
    'Gemini': 'စကားကောင်းသူ၊ လိမ္မာပါးနပ်သူ',
    'Cancer': 'စာနာတတ်သူ၊ မိသားစုကိုတန်ဖိုးထားသူ',
    'Leo': 'မာန်မာနရှိသူ၊ ခေါင်းဆောင်ဖြစ်ချင်သူ',
    'Virgo': 'ပြည့်စုံပြီးပြည့်စုံသူ၊ အသေးစိတ်ဂရုစိုက်သူ',
    'Libra': 'ဟန်ချက်ညီသူ၊ တရားမျှတမှုကြိုက်သူ',
    'Scorpio': 'စိတ်အားကြီးမားသူ၊ စွဲမြဲစွာကြိုးစားသူ',
    'Sagittarius': 'စွန့်စားရဲသူ၊ လွတ်လပ်မှုကြိုက်သူ',
    'Capricorn': 'ရည်မှန်းချက်ရှိသူ၊ တာဝန်ယူတတ်သူ',
    'Aquarius': 'ထူးခြားသူ၊ လူမှုရေးအတွက်ကြိုးစားသူ',
    'Pisces': 'စိတ်ကူးကြွသူ၊ စာနာတတ်သူ'
}

def get_character_description(character: Character) -> str:
    """Generate simple pre-defined character description
    
    Args:
        character: Character object
        
    Returns:
        Description in Burmese
    """
    mbti_desc = MBTI_DESCRIPTIONS.get(character.mbti, 'ထူးခြားသော လက္ခဏာရှိသူ')
    zodiac_desc = ZODIAC_DESCRIPTIONS.get(character.zodiac, 'စိတ်ဓာတ်ကောင်းသူ')
    
    return f"{mbti_desc}၊ {zodiac_desc}"


class VotingHandler:
    """Handles voting operations"""
    
    def __init__(self):
        # Store active votes: {game_id: {round: {team: {user_id: character_id}}}}
        # Note: Dict maintains insertion order in Python 3.7+ for vote order tracking
        self.active_votes: Dict[int, Dict[int, Dict[int, Dict[int, int]]]] = {}
        # Store round start times: {game_id: {round: datetime}}
        self.round_timers: Dict[int, Dict[int, datetime]] = {}
        # Store voting messages: {game_id: {round: {team: {user_id: message_id}}}}
        self.voting_messages: Dict[int, Dict[int, Dict[int, Dict[int, int]]]] = {}
    
    def init_game_voting(self, game_id: int):
        """Initialize voting data for a game"""
        logger.debug(f"Initializing voting for game {game_id}")
        if game_id not in self.active_votes:
            self.active_votes[game_id] = {}
            self.round_timers[game_id] = {}
            self.voting_messages[game_id] = {}
    
    def init_round_voting(self, game_id: int, round_number: int):
        """Initialize voting for a round"""
        logger.debug(f"Initializing voting for game {game_id}, round {round_number}")
        self.init_game_voting(game_id)
        if round_number not in self.active_votes[game_id]:
            self.active_votes[game_id][round_number] = {}
            self.round_timers[game_id][round_number] = datetime.now()
            self.voting_messages[game_id][round_number] = {}
    
    async def create_voting_message(self, characters: List[Character], 
                                   role: str, role_description: str,
                                   team_id: int, team_players: List[Dict[str, Any]],
                                   current_user_id: int) -> str:
        """Create voting message with team and character info"""
        # Team Info Header
        team_name = get_team_name(team_players)
        lines = [
            f"👥 **{team_name}**"
        ]
        
        # Show team players
        for player in team_players:
            username = player.get('username', 'Unknown')
            user_id = player.get('user_id')
            is_leader = player.get('is_leader', False)
            
            if user_id == current_user_id:
                prefix = "➤" if is_leader else "•"
                lines.append(f"  {prefix} @{username} (You)" + (" 👑" if is_leader else ""))
            else:
                prefix = "👑" if is_leader else "•"
                lines.append(f"  {prefix} @{username}")
        
        lines.append("")
        lines.append(f"📋 **Round Voting: {role}**")
        lines.append(f"*{role_description}*\n")
        lines.append("Character များထဲက အသင့်တော်ဆုံးကို ရွေးချယ်ပါ:")
        lines.append("(သို့မဟုတ်) 🎲 Random character ကို ရွေးချယ်နိုင်ပါသည်။\n")
        
        for i, char in enumerate(characters, 1):
            # Get pre-defined description
            description = get_character_description(char)
            
            lines.append(f"**{i}. {char.name}**")
            lines.append(f"   MBTI: {char.mbti} | Zodiac: {char.zodiac}")
            lines.append(f"   {description}\n")
        
        lines.append(f"⏰ Time: {config.ROUND_TIME} seconds")
        
        return "\n".join(lines)
    
    def create_voting_keyboard(self, game_id: int, round_number: int, 
                              team_id: int, characters: List[Character]) -> InlineKeyboardMarkup:
        """Create voting keyboard with 5 characters + dice option"""
        keyboard = []
        
        # Add buttons for each character
        for i, char in enumerate(characters, 1):
            button = InlineKeyboardButton(
                f"✅ {char.name}",
                callback_data=f"vote_{game_id}_{round_number}_{team_id}_{char.id}"
            )
            keyboard.append([button])
        
        # Add dice button for random selection
        dice_button = InlineKeyboardButton(
            "🎲 Random Character",
            callback_data=f"vote_{game_id}_{round_number}_{team_id}_dice"
        )
        keyboard.append([dice_button])
        
        return InlineKeyboardMarkup(keyboard)
    
    async def send_team_voting(self, context: ContextTypes.DEFAULT_TYPE, 
                              game_id: int, round_number: int, team_id: int,
                              team_players: List[Dict[str, Any]], 
                              characters: List[Character]):
        """Send voting message to all players in a team"""
        logger.info(f"Sending voting to team {team_id} - Game: {game_id}, Round: {round_number}")
        self.init_round_voting(game_id, round_number)
        
        if team_id not in self.active_votes[game_id][round_number]:
            self.active_votes[game_id][round_number][team_id] = {}
            self.voting_messages[game_id][round_number][team_id] = {}
        
        # Get role info from theme
        theme_id = await db_manager.get_game_theme(game_id)
        theme = get_theme_by_id(theme_id)
        role_info = theme['roles'].get(round_number, {})
        role_name = role_info.get('name', 'Unknown')
        role_description = role_info.get('description', '')
        
        # Create keyboard (same for all)
        keyboard = self.create_voting_keyboard(game_id, round_number, team_id, characters)
        
        # Calculate adaptive delay based on team size
        # More players = longer delay to avoid rate limits
        team_size = len(team_players)
        if team_size <= 3:
            base_delay = 0.8  # 800ms for small teams
        elif team_size <= 4:
            base_delay = 1.0  # 1 second for medium teams
        else:
            base_delay = 1.2  # 1.2 seconds for large teams
        
        logger.debug(f"Team {team_id} has {team_size} players, using {base_delay}s delay between messages")
        
        # Send to each player with personalized message (with retry logic)
        for i, player in enumerate(team_players):
            user_id = player['user_id']
            
            # Add adaptive delay between messages (except first message)
            if i > 0:
                await asyncio.sleep(base_delay)
            
            # Create personalized message for this player
            message_text = await self.create_voting_message(
                characters, role_name, role_description,
                team_id, team_players, user_id
            )
            
            # Send with retry logic for reliable delivery
            msg = await message_delivery.send_message_with_retry(
                context.bot,
                chat_id=user_id,
                text=message_text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            
            if msg:
                self.voting_messages[game_id][round_number][team_id][user_id] = msg.message_id
                logger.debug(f"Voting message delivered to user {user_id}")
            else:
                logger.error(f"Failed to deliver voting message to user {user_id} after all retries")
    
    async def handle_vote(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
        """Handle a vote submission (including dice roll)
        
        Returns:
            True if vote was recorded
        """
        query = update.callback_query
        
        # Parse callback data
        vote_data = parse_vote_callback(query.data)
        if not vote_data:
            logger.warning(f"Invalid vote callback data: {query.data}")
            await query.answer("⚠️ Invalid vote data", show_alert=True)
            return False
        
        game_id = vote_data['game_id']
        round_number = vote_data['round']
        team_id = vote_data['team']
        character_id = vote_data['character_id']
        user_id = query.from_user.id
        
        # Handle dice roll - select random character
        if character_id == 'dice':
            import random
            # Get all characters from database
            all_characters = await db_manager.get_all_characters()
            if not all_characters:
                await query.answer("❌ No characters available!", show_alert=True)
                return False
            
            # Select random character
            random_character = random.choice(all_characters)
            character_id = random_character.id
            logger.info(f"Dice roll - User {user_id} got random character: {random_character.name} (ID: {character_id})")
            await query.answer(f"🎲 Random: {random_character.name}!")
        
        # Check if voting time has expired
        self.init_round_voting(game_id, round_number)
        
        if game_id in self.round_timers and round_number in self.round_timers[game_id]:
            round_start_time = self.round_timers[game_id][round_number]
            elapsed_time = (datetime.now() - round_start_time).total_seconds()
            
            if elapsed_time > config.ROUND_TIME:
                logger.warning(f"Late vote rejected - Game: {game_id}, Round: {round_number}, User: {user_id}, Elapsed: {elapsed_time}s")
                await query.answer(
                    "⏱️ Voting time ကျော်သွားပါပြီ!\n\n"
                    "Late votes များကို လက်မခံပါ။",
                    show_alert=True
                )
                return False
        
        await query.answer("မဲပေးပြီးပါပြီ! ✅")
        
        # Record vote
        
        if team_id not in self.active_votes[game_id][round_number]:
            self.active_votes[game_id][round_number][team_id] = {}
        
        self.active_votes[game_id][round_number][team_id][user_id] = character_id
        logger.info(f"Vote recorded - Game: {game_id}, Round: {round_number}, Team: {team_id}, User: {user_id}, Character: {character_id}")
        
        # Get voter info
        voter_username = query.from_user.username or query.from_user.first_name or f"User_{user_id}"
        
        # Update message to show vote recorded
        try:
            character = await db_manager.get_character(character_id)
            # Get role name for this round from theme
            theme_id = await db_manager.get_game_theme(game_id)
            theme = get_theme_by_id(theme_id)
            role_info = theme['roles'].get(round_number, {})
            role_name = role_info.get('name', 'Unknown')
            
            await query.edit_message_text(
                f"✅ သင်က **{character.name}** ကို **{role_name}** အတွက် ရွေးချယ်ပြီးပါပြီ!\n\nအခြား player များကို စောင့်နေပါသည်...",
                parse_mode='Markdown'
            )
            
            # Notify team members about this vote
            # Get team players from game handler
            from handlers.game_handler import game_handler
            if user_id in game_handler.player_teams:
                team_info = game_handler.player_teams[user_id]
                team_players = team_info['team_players']
                team_name = get_team_name(team_players)
                
                # Send notification to other team members (with retry logic)
                for player in team_players:
                    recipient_id = player.get('user_id')
                    if recipient_id != user_id:  # Don't send to voter
                        notification = await message_delivery.send_message_with_retry(
                            context.bot,
                            chat_id=recipient_id,
                            text=f"📢 **{team_name} Vote Update**\n\n"
                                 f"@{voter_username} က **{character.name}** ကို "
                                 f"**{role_name}** အတွက် vote လုပ်ပြီးပါပြီ။",
                            parse_mode='Markdown'
                        )
                        
                        if notification:
                            logger.debug(f"Vote notification delivered to team member {recipient_id}")
                        else:
                            logger.error(f"Failed to deliver vote notification to {recipient_id}")
        except Exception as e:
            logger.error(f"Error updating vote message: {e}")
        
        return True
    
    def get_team_votes(self, game_id: int, round_number: int, team_id: int) -> Dict[int, int]:
        """Get all votes for a team in a round"""
        if game_id not in self.active_votes:
            return {}
        if round_number not in self.active_votes[game_id]:
            return {}
        if team_id not in self.active_votes[game_id][round_number]:
            return {}
        
        return self.active_votes[game_id][round_number][team_id]
    
    def resolve_team_vote(self, votes: Dict[int, int], team_players: List[Dict[str, Any]]) -> Optional[int]:
        """Resolve team vote to select character
        
        Logic:
        - If 2+ votes for same character → select it (majority)
        - If all different votes:
            * Leader voted → use leader's vote
            * Leader didn't vote → use first voter's vote
        - If no votes → return None (Optional)
        
        Args:
            votes: Dict mapping user_id to character_id (maintains insertion order)
            team_players: List of team players (with is_leader flag)
            
        Returns:
            Selected character_id or None
        """
        if not votes:
            return None
        
        # Find leader's user_id and vote
        leader_user_id = None
        leader_vote = None
        for player in team_players:
            if player.get('is_leader', False):
                leader_user_id = player.get('user_id')
                if leader_user_id in votes:
                    leader_vote = votes[leader_user_id]
                break
        
        # Count votes per character
        vote_counts = {}
        for user_id, char_id in votes.items():
            if char_id not in vote_counts:
                vote_counts[char_id] = 0
            vote_counts[char_id] += 1
        
        # Check for majority (2+ votes for same character)
        for char_id, count in vote_counts.items():
            if count >= 2:
                logger.debug(f"Majority vote: Character {char_id} with {count} votes")
                return char_id
        
        # No majority - all different votes
        # Priority: Leader's vote > First voter's vote
        if leader_vote is not None:
            logger.debug(f"No majority, using leader's vote: Character {leader_vote}")
            return leader_vote
        else:
            # Leader didn't vote, use first voter's choice
            first_vote = list(votes.values())[0]
            logger.debug(f"No majority, leader didn't vote, using first voter's choice: Character {first_vote}")
            return first_vote
    
    async def finalize_round_voting(self, game_id: int, round_number: int, 
                                   teams: Dict[int, List[Dict[str, Any]]],
                                   context: ContextTypes.DEFAULT_TYPE = None) -> Dict[int, Optional[int]]:
        """Finalize voting for all teams in a round
        
        Returns:
            Dict mapping team_id to selected character_id
        """
        logger.info(f"Finalizing voting - Game: {game_id}, Round: {round_number}")
        selections = {}
        
        # Get role info from theme
        theme_id = await db_manager.get_game_theme(game_id)
        theme = get_theme_by_id(theme_id)
        role_info = theme['roles'].get(round_number, {})
        role_name = role_info.get('name', 'Unknown')
        
        for team_id, team_players in teams.items():
            votes = self.get_team_votes(game_id, round_number, team_id)
            selected_char_id = self.resolve_team_vote(votes, team_players)
            logger.debug(f"Team {team_id} selection: Character {selected_char_id} (Votes: {votes})")
            
            selections[team_id] = selected_char_id
            
            # Send notification to players who didn't vote
            if context:
                for player in team_players:
                    user_id = player.get('user_id')
                    if user_id not in votes:
                        # Player didn't vote
                        try:
                            await context.bot.send_message(
                                chat_id=user_id,
                                text=f"⚠️ **Round {round_number} Voting Skipped**\n\n"
                                     f"သင် Round {round_number} ({role_name}) အတွက် "
                                     f"vote မပေးခဲ့ပါ!\n\n"
                                     f"နောက် round မှာ မမေ့ပဲ vote ပေးပါနော်။",
                                parse_mode='Markdown'
                            )
                            logger.debug(f"Sent skip notification to user {user_id}")
                        except Exception as e:
                            logger.error(f"Failed to send skip notification to user {user_id}: {e}")
                
                # Send final selection confirmation to all team members
                team_name = get_team_name(team_players)
                if selected_char_id:
                    character = await db_manager.get_character(selected_char_id)
                    confirmation_msg = (
                        f"✅ {team_name} - Round {round_number} ရလဒ်\n\n"
                        f"📊 {role_name} အတွက်:\n"
                        f"➡️ {character.name} ကို ရွေးချယ်ပြီးပါပြီ!\n\n"
                    )
                    
                    # Show voting summary
                    if votes:
                        confirmation_msg += "🗳️ Voting Summary:\n"
                        for voter_id, char_id in votes.items():
                            voter_player = next((p for p in team_players if p['user_id'] == voter_id), None)
                            if voter_player:
                                voter_name = voter_player.get('username', 'Unknown')
                                voted_char = await db_manager.get_character(char_id)
                                leader_mark = " 👑" if voter_player.get('is_leader') else ""
                                confirmation_msg += f"• {voter_name}{leader_mark} → {voted_char.name}\n"
                else:
                    confirmation_msg = (
                        f"⚠️ {team_name} - Round {round_number} ရလဒ်\n\n"
                        f"{role_name} အတွက်: Optional\n"
                        f"(Team က vote မပေးခဲ့ပါ)"
                    )
                
                # Send confirmation to all team members (without Markdown to avoid parsing errors)
                for player in team_players:
                    user_id = player.get('user_id')
                    try:
                        await context.bot.send_message(
                            chat_id=user_id,
                            text=confirmation_msg
                        )
                        logger.debug(f"Sent selection confirmation to user {user_id}")
                    except Exception as e:
                        logger.error(f"Failed to send confirmation to user {user_id}: {e}")
            
            # Save to database
            if selected_char_id:
                await db_manager.save_round_selection(
                    game_id, round_number, team_id, role_name, 
                    selected_char_id, votes
                )
        
        return selections
    
    def clear_game_votes(self, game_id: int):
        """Clear voting data for a game"""
        logger.debug(f"Clearing votes for game {game_id}")
        if game_id in self.active_votes:
            del self.active_votes[game_id]
        if game_id in self.round_timers:
            del self.round_timers[game_id]
        if game_id in self.voting_messages:
            del self.voting_messages[game_id]


# Global voting handler instance
voting_handler = VotingHandler()


