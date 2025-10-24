"""
Game flow handler
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from typing import Dict, List, Any
import asyncio
import logging
from database.db_manager import db_manager
from services.team_service import team_service
from services.scoring_service import scoring_service
from handlers.voting_handler import voting_handler
from utils.constants import GAME_STATUS
from utils.helpers import get_team_name
from utils.message_delivery import message_delivery
from data.themes import get_random_theme, get_theme_by_id
import config

# Setup logger
logger = logging.getLogger(__name__)


class GameHandler:
    """Handles game flow and state management"""
    
    def __init__(self):
        self.num_rounds = config.NUM_ROUNDS
        self.round_time = config.ROUND_TIME
        self.characters_per_round = config.CHARACTERS_PER_VOTING
        # Store active games: {game_id: {'teams': ..., 'chat_id': ..., 'message_id': ...}}
        self.active_games: Dict[int, Dict[str, Any]] = {}
        # Store player team info for chat: {user_id: {'game_id': ..., 'team_id': ..., 'team_players': [...]}}
        self.player_teams: Dict[int, Dict[str, Any]] = {}
        # Store game themes: {game_id: theme_dict}
        self.game_themes: Dict[int, Dict[str, Any]] = {}
    
    async def start_game(self, context: ContextTypes.DEFAULT_TYPE, 
                        lobby_chat_id: int, lobby_message_id: int) -> int:
        """Start a new game
        
        Returns:
            game_id
        """
        logger.info(f"Starting new game - Chat: {lobby_chat_id}, Message: {lobby_message_id}")
        
        # Get players from lobby
        players = await db_manager.get_lobby_players()
        logger.debug(f"Retrieved {len(players)} players from lobby")
        
        if len(players) < config.MIN_PLAYERS:
            logger.warning(f"Not enough players to start game: {len(players)} (minimum: {config.MIN_PLAYERS})")
            return None
        
        # Select random theme
        theme = get_random_theme()
        logger.info(f"Selected theme: {theme['emoji']} {theme['name']} (ID: {theme['id']})")
        
        # Create game with theme
        game_id = await db_manager.create_game(lobby_message_id, lobby_chat_id, theme['id'])
        logger.info(f"Game created with ID: {game_id}")
        
        # Store theme in memory
        self.game_themes[game_id] = theme
        
        # Form teams
        teams = team_service.form_teams(players)
        logger.info(f"Teams formed - {len(teams)} teams created")
        
        # Save teams to database
        flat_players = team_service.flatten_teams_for_db(teams)
        await db_manager.add_game_players(game_id, flat_players)
        
        # Clear lobby
        await db_manager.clear_lobby()
        
        # Update game status
        await db_manager.update_game_status(game_id, GAME_STATUS['IN_PROGRESS'])
        
        # Store game data
        self.active_games[game_id] = {
            'teams': teams,
            'chat_id': lobby_chat_id,
            'message_id': lobby_message_id,
            'team_announcement_message_id': None,
            'round_messages': {}  # {round_number: message_id}
        }
        
        # Store player team info for team chat
        for team_id, team_players in teams.items():
            for player in team_players:
                user_id = player.get('user_id')
                self.player_teams[user_id] = {
                    'game_id': game_id,
                    'team_id': team_id,
                    'team_players': team_players
                }
        
        logger.debug(f"Stored team info for {len(self.player_teams)} players")
        
        # Announce teams with theme (no parse_mode to avoid underscore issues in usernames)
        team_announcement = team_service.get_team_announcement_message(teams)
        # Add theme info at the beginning
        theme_announcement = f"{theme['emoji']} Theme: {theme['name']}\n\n{team_announcement}"
        msg = await context.bot.send_message(
            chat_id=lobby_chat_id,
            text=theme_announcement
        )
        self.active_games[game_id]['team_announcement_message_id'] = msg.message_id
        logger.debug(f"Team announcement message ID: {msg.message_id}")
        
        # Wait a moment before starting rounds
        await asyncio.sleep(3)
        
        # Start rounds
        await self.run_all_rounds(context, game_id)
        
        return game_id
    
    async def run_all_rounds(self, context: ContextTypes.DEFAULT_TYPE, game_id: int):
        """Run all 5 rounds of the game"""
        logger.info(f"Starting rounds for game {game_id}")
        game_data = self.active_games.get(game_id)
        if not game_data:
            logger.error(f"Game {game_id} not found in active games")
            return
        
        teams = game_data['teams']
        chat_id = game_data['chat_id']
        
        # Run each round
        for round_number in range(1, self.num_rounds + 1):
            logger.info(f"Game {game_id} - Starting round {round_number}/{self.num_rounds}")
            await self.run_round(context, game_id, round_number, teams, chat_id)
            
            # Wait between rounds
            if round_number < self.num_rounds:
                await asyncio.sleep(2)
        
        # Game finished, show results
        await self.finish_game(context, game_id, teams, chat_id)
    
    async def run_round(self, context: ContextTypes.DEFAULT_TYPE, game_id: int, 
                       round_number: int, teams: Dict[int, List[Dict[str, Any]]], 
                       chat_id: int):
        """Run a single round"""
        logger.debug(f"Game {game_id} - Running round {round_number}")
        
        # Update game round
        await db_manager.update_game_round(game_id, round_number)
        
        # Get role info from theme
        theme = self.game_themes.get(game_id)
        if not theme:
            # Fallback: load from database if not in memory
            theme_id = await db_manager.get_game_theme(game_id)
            theme = get_theme_by_id(theme_id)
            self.game_themes[game_id] = theme
        
        role_info = theme['roles'].get(round_number, {})
        role_name = role_info.get('name', 'Unknown')
        
        # Announce round start with "Go to Bot" button
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        
        bot_username = (await context.bot.get_me()).username
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🤖 Go to Bot", url=f"https://t.me/{bot_username}")]
        ])
        
        round_message = f"""🎯 **ROUND {round_number}/5**

👑 Role: **{role_name}**

✅ Voting စတင်ပါပြီ!
⏱️  Time: {self.round_time} စက္ကန့်

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
👉 Bot ထံသို့ သွားပြီး vote ပေးပါ!"""
        
        # Always send new message for each round
        msg = await context.bot.send_message(
            chat_id=chat_id,
            text=round_message,
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
        
        # Store this round's message ID
        game_data = self.active_games.get(game_id)
        if 'round_messages' not in game_data:
            game_data['round_messages'] = {}
        game_data['round_messages'][round_number] = msg.message_id
        logger.debug(f"Sent round {round_number} message {msg.message_id}")
        
        # Initialize voting for this round
        voting_handler.init_round_voting(game_id, round_number)
        
        # Send voting to each team
        for team_id, team_players in teams.items():
            # Get characters already used by this team
            used_character_ids = await db_manager.get_team_used_character_ids(game_id, team_id)
            
            # Get random characters (excluding already used ones)
            characters = await db_manager.get_random_characters(
                self.characters_per_round, 
                exclude_ids=used_character_ids
            )
            
            if len(characters) < self.characters_per_round:
                logger.error(f"Not enough characters in database: {len(characters)}/{self.characters_per_round}")
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"⚠️ Database မှာ character အရေအတွက် မလုံလောက်ပါ! အနည်းဆုံး {self.characters_per_round} characters လိုအပ်ပါတယ်။"
                )
                return
            
            logger.debug(f"Game {game_id} - Team {team_id} - Sending voting for round {round_number} (excluded {len(used_character_ids)} used characters)")
            
            # Send voting messages
            await voting_handler.send_team_voting(
                context, game_id, round_number, team_id, team_players, characters
            )
        
        # Wait for voting time
        logger.debug(f"Game {game_id} - Round {round_number} - Waiting {self.round_time} seconds for votes")
        await asyncio.sleep(self.round_time)
        
        # Finalize votes
        logger.debug(f"Game {game_id} - Round {round_number} - Finalizing votes")
        selections = await voting_handler.finalize_round_voting(game_id, round_number, teams, context)
        
        # Announce selections
        await self.announce_round_results(context, chat_id, round_number, selections, teams, game_id)
    
    async def announce_round_results(self, context: ContextTypes.DEFAULT_TYPE, 
                                    chat_id: int, round_number: int, 
                                    selections: Dict[int, int], 
                                    teams: Dict[int, List[Dict[str, Any]]],
                                    game_id: int):
        """Announce round results by editing the round message with individual votes"""
        # Get role info from theme
        theme = self.game_themes.get(game_id)
        if not theme:
            theme_id = await db_manager.get_game_theme(game_id)
            theme = get_theme_by_id(theme_id)
            self.game_themes[game_id] = theme
        
        role_info = theme['roles'].get(round_number, {})
        role_name = role_info.get('name', 'Unknown')
        
        lines = [
            f"✅ ROUND {round_number}/5 COMPLETED",
            "",
            f"👑 Role: {role_name}",
            "",
            "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬",
            "📊 Team Selections:",
            ""
        ]
        
        for team_id in sorted(teams.keys()):
            team_name = get_team_name(teams[team_id])
            char_id = selections.get(team_id)
            
            # Get the final selected character
            if char_id:
                character = await db_manager.get_character(char_id)
                char_name = character.name if character else "Unknown"
            else:
                char_name = "No selection"
            
            lines.append(f"✓ {team_name}")
            lines.append(f"   → Final: {char_name}")
            
            # Get individual votes
            votes = await db_manager.get_round_votes(game_id, round_number, team_id)
            if votes:
                lines.append(f"   📝 Individual votes:")
                for user_id, voted_char_id in votes.items():
                    # Get player info
                    player = next((p for p in teams[team_id] if p['user_id'] == int(user_id)), None)
                    if player:
                        username = player.get('username', f"User_{user_id}")
                        # Get voted character
                        voted_char = await db_manager.get_character(voted_char_id)
                        voted_char_name = voted_char.name if voted_char else "Unknown"
                        leader_mark = " 👑" if player.get('is_leader') else ""
                        lines.append(f"      • {username}{leader_mark} → {voted_char_name}")
            
            lines.append("")
        
        lines.append("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
        message = "\n".join(lines)
        
        # Edit this round's message with results (without Markdown to avoid parsing errors)
        game_data = self.active_games.get(game_id)
        if game_data and 'round_messages' in game_data and round_number in game_data['round_messages']:
            try:
                await context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=game_data['round_messages'][round_number],
                    text=message
                )
                logger.debug(f"Edited round {round_number} message with results")
            except Exception as e:
                logger.error(f"Error editing round results: {e}")
    
    async def send_private_results(self, context: ContextTypes.DEFAULT_TYPE, 
                                   game_id: int, teams: Dict[int, List[Dict[str, Any]]],
                                   results: Dict[int, Dict[str, Any]], winner: int):
        """Send private results to all players"""
        logger.info(f"Game {game_id} - Sending private results to all players")
        
        # Prepare winner info
        winner_team_name = get_team_name(results[winner]['players'])
        winner_score = results[winner]['total_score']
        
        for team_id, team_players in teams.items():
            team_name = get_team_name(team_players)
            team_data = results.get(team_id, {})
            team_score = team_data.get('total_score', 0)
            
            # Build team result message
            lines = [
                "📊 **YOUR RESULTS**",
                "",
                f"**{team_name}**",
                f"🎮 Game ID: {game_id}",
                ""
            ]
            
            # Show team's rounds
            if 'rounds' in team_data:
                lines.append("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
                lines.append("📋 **Round Results:**")
                lines.append("")
                
                for round_data in team_data['rounds']:
                    role = round_data.get('role', 'Unknown')
                    char_name = round_data.get('character_name', 'Optional')
                    score = round_data.get('score', 0)
                    lines.append(f"**{role}**")
                    lines.append(f"  → {char_name}")
                    lines.append(f"  → Score: {score}/10 မှတ်")
                    lines.append("")
                
                lines.append("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
                lines.append(f"💯 **Total Score:** {team_score} မှတ်")
                lines.append("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
                lines.append("")
            
            # Show winner
            if team_id == winner:
                lines.append("🎉🎉🎉🎉🎉🎉🎉")
                lines.append("**🏆 WINNER! 🏆**")
                lines.append("🎉🎉🎉🎉🎉🎉🎉")
                lines.append("")
                lines.append("**သင့် Team က အနိုင်ရခဲ့ပါတယ်!**")
                lines.append("Congratulations!")
            else:
                lines.append("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
                lines.append(f"👑 **Winner:** {winner_team_name}")
                lines.append(f"💯 Score: {winner_score} မှတ်")
                lines.append("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
            
            private_message = "\n".join(lines)
            
            # Send to all players in team (with retry logic)
            for player in team_players:
                user_id = player.get('user_id')
                
                result_msg = await message_delivery.send_message_with_retry(
                    context.bot,
                    chat_id=user_id,
                    text=private_message,
                    parse_mode='Markdown'
                )
                
                if result_msg:
                    logger.debug(f"Private result delivered to user {user_id}")
                else:
                    logger.error(f"Failed to deliver private result to user {user_id}")
            
            # Small delay between teams
            await asyncio.sleep(1)
    
    async def finish_game(self, context: ContextTypes.DEFAULT_TYPE, game_id: int,
                         teams: Dict[int, List[Dict[str, Any]]], chat_id: int):
        """Finish game and show results"""
        logger.info(f"Game {game_id} - Finishing game and calculating results")
        
        # Score the game
        results = await scoring_service.score_game(game_id)
        logger.debug(f"Game {game_id} - Scoring completed")
        
        # Determine winner
        winner = scoring_service.determine_winner(results)
        logger.info(f"Game {game_id} - Winner determined: Team {winner}")
        
        # Save winner
        await db_manager.set_game_winner(game_id, winner)
        
        # Announce game finished
        calculating_msg = await context.bot.send_message(
            chat_id=chat_id,
            text="""🏁 GAME FINISHED

⏳ ရလဒ်များကို တွက်ချက်နေပါသည်...

🔢 Scoring in progress..."""
        )
        
        # Wait a moment for drama
        await asyncio.sleep(3)
        
        # Edit calculating message to show "ရလဒ်များ:"
        try:
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=calculating_msg.message_id,
                text="""🏁 GAME FINISHED

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
📊 FINAL RESULTS
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

↓ ရလဒ်များကို အောက်တွင် ကြည့်ပါ"""
            )
            logger.debug(f"Edited calculating message to show results header")
        except Exception as e:
            logger.error(f"Error editing calculating message: {e}")
        
        # Send results for each team with details button
        result_messages = scoring_service.format_all_results(results, winner)
        
        for team_id, message in zip(sorted(results.keys()), result_messages):
            # Create details button for each team
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📊 Details", callback_data=f"details_{game_id}_{team_id}")]
            ])
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=message,
                reply_markup=keyboard
            )
            await asyncio.sleep(1)
        
        # Final winner announcement
        winner_players = results[winner]['players']
        winner_team_name = get_team_name(winner_players)
        winner_score = results[winner]['total_score']
        
        # Format winner names with leader mark
        winner_names_list = []
        for player in winner_players:
            username = player.get('username', 'Unknown')
            leader_mark = " 👑" if player.get('is_leader') else ""
            winner_names_list.append(f"{username}{leader_mark}")
        winner_names = ', '.join(winner_names_list)
        
        final_message = f"""
🎉🎉🎉🎉🎉🎉🎉
🏆 အနိုင်ရရှိသူ! 🏆
🎉🎉🎉🎉🎉🎉🎉

👑 {winner_team_name} 👑

Players: {winner_names}

💯 Final Score: {winner_score} မှတ်

Congratulations! 🎊
Game ပါဝင်ကစားပေးတဲ့အတွက် ကျေးဇူးတင်ပါတယ်! 🙏
"""
        
        await context.bot.send_message(
            chat_id=chat_id,
            text=final_message
        )
        
        # Send private results to all players
        logger.debug(f"Game {game_id} - Sending private results to all players")
        await self.send_private_results(context, game_id, teams, results, winner)
        
        # Update game status to finished
        await db_manager.update_game_status(game_id, GAME_STATUS['FINISHED'])
        logger.info(f"Game {game_id} - Status updated to finished")
        
        # Cleanup
        voting_handler.clear_game_votes(game_id)
        
        # Clear player teams
        players_to_remove = [user_id for user_id, data in self.player_teams.items() 
                            if data['game_id'] == game_id]
        for user_id in players_to_remove:
            del self.player_teams[user_id]
        logger.debug(f"Cleared team info for {len(players_to_remove)} players")
        
        if game_id in self.active_games:
            del self.active_games[game_id]
        
        logger.info(f"Game {game_id} - Game completed and cleaned up")


# Global game handler instance
game_handler = GameHandler()


