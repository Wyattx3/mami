"""
Lobby handler for join/quit operations
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Optional
from database.db_manager import db_manager
from utils.helpers import format_player_list
import config

# Setup logger
logger = logging.getLogger(__name__)


class LobbyHandler:
    """Handles lobby operations with dynamic sizing and timer"""
    
    def __init__(self):
        self.min_players = config.MIN_PLAYERS
        self.max_players = config.MAX_PLAYERS
        self.lobby_timeout = config.LOBBY_TIMEOUT
        
        # Track lobby timer
        self.lobby_start_time: Optional[datetime] = None
        self.lobby_chat_id: Optional[int] = None
        self.lobby_message_id: Optional[int] = None
        self.timer_task: Optional[asyncio.Task] = None
    
    async def create_lobby_message(self, update: Update = None, players: list = None) -> str:
        """Create lobby message with current players and timer"""
        if players is None:
            players = await db_manager.get_lobby_players()
        count = len(players)
        
        # Calculate remaining time
        time_remaining = "N/A"
        if self.lobby_start_time:
            elapsed = (datetime.now() - self.lobby_start_time).total_seconds()
            remaining = max(0, self.lobby_timeout - elapsed)
            time_remaining = f"{int(remaining)}s"
        
        message_lines = [
            "🎮 **GAME LOBBY**",
            "",
            f"👥 Players: **{count}** (Min: {self.min_players}, Max: {self.max_players})",
            f"⏱️ Time: **{time_remaining}**",
            "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"
        ]
        
        # Status message
        if count < self.min_players:
            needed = self.min_players - count
            message_lines.append(f"\n⚠️ အနည်းဆုံး {needed} ယောက် ထပ်လိုအပ်ပါသည်")
        elif count >= self.min_players:
            # Calculate teams
            num_teams = count // config.TEAM_SIZE
            excess = count % config.TEAM_SIZE
            if excess > 0:
                message_lines.append(f"\n✅ စတင်နိုင်ပါပြီ! (Teams: {num_teams}, Excess: {excess})")
                message_lines.append(f"⚠️ Timer ပြီးရင် excess {excess} ယောက်ကို ဖြုတ်ပြီး စတင်မည်")
            else:
                message_lines.append(f"\n✅ အဆင်သင့်! (Teams: {num_teams})")
        
        message_lines.append("")
        
        if players:
            message_lines.append(format_player_list(players))
        else:
            message_lines.append("⚠️ No players yet")
        
        message_lines.append("")
        message_lines.append("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
        message_lines.append("👇 Click button to join!")
        
        return "\n".join(message_lines)
    
    def get_lobby_keyboard(self) -> InlineKeyboardMarkup:
        """Get lobby inline keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("✅ Join Game", callback_data="join_lobby"),
                InlineKeyboardButton("❌ Quit Game", callback_data="quit_lobby")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    async def handle_join(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
        """Handle player joining lobby
        
        Returns:
            True if lobby is full and game should start
        """
        query = update.callback_query
        await query.answer()
        
        user = query.from_user
        user_id = user.id
        username = user.username or user.first_name or f"User_{user_id}"
        logger.debug(f"Player attempting to join lobby: {username} (ID: {user_id})")
        
        # Check if user is already in another active game
        is_in_game = await db_manager.is_user_in_active_game(user_id)
        if is_in_game:
            logger.warning(f"User {user_id} tried to join but is already in active game")
            await query.answer(
                "⚠️ သင်သည် လက်ရှိ game တခုထဲမှာ ပါဝင်နေပါသည်!\n\n"
                "Game တပွဲပြီးမှ နောက်တပွဲ ဆော့နိုင်ပါမယ်။",
                show_alert=True
            )
            return False
        
        # Add to lobby
        added = await db_manager.add_to_lobby(user_id, username)
        
        if not added:
            logger.info(f"Player already in lobby: {username}")
            await query.answer("သင် lobby ထဲမှာ ရှိပြီးသားပါ!", show_alert=True)
            return False
        
        logger.info(f"Player joined lobby: {username}")
        
        # Update message
        lobby_message = await self.create_lobby_message(update)
        await query.edit_message_text(
            text=lobby_message,
            reply_markup=self.get_lobby_keyboard()
        )
        
        # Check if lobby is full
        count = await db_manager.get_lobby_count()
        logger.debug(f"Lobby count: {count}/{self.lobby_size}")
        if count >= self.lobby_size:
            logger.info(f"Lobby full! Starting game with {count} players")
            return True
        
        return False
    
    async def handle_quit(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
        """Handle player quitting lobby"""
        query = update.callback_query
        await query.answer()
        
        user = query.from_user
        user_id = user.id
        logger.debug(f"Player attempting to quit lobby: User ID {user_id}")
        
        # Remove from lobby
        removed = await db_manager.remove_from_lobby(user_id)
        
        if not removed:
            logger.info(f"Player not in lobby: User ID {user_id}")
            await query.answer("သင် lobby ထဲမှာ မရှိပါဘူး!", show_alert=True)
            return False
        
        logger.info(f"Player quit lobby: User ID {user_id}")
        
        # Update message
        lobby_message = await self.create_lobby_message(update)
        await query.edit_message_text(
            text=lobby_message,
            reply_markup=self.get_lobby_keyboard()
        )
        
        return True
    
    async def announce_game_start(self, context: ContextTypes.DEFAULT_TYPE, 
                                 chat_id: int, message_id: int):
        """Announce that game is starting"""
        message = """🎮 **GAME STARTING**

✅ Player အရေအတွက် ပြည့်ပါပြီ

⏳ Team များ ခွဲခြားနေပါသည်...

Please wait..."""
        
        try:
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=message
            )
        except Exception as e:
            print(f"Error announcing game start: {e}")


# Global lobby handler instance
lobby_handler = LobbyHandler()


