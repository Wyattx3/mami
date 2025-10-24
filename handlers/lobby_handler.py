"""
Lobby handler for join/quit operations
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import BadRequest
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
    
    async def start_lobby_timer(self, context: ContextTypes.DEFAULT_TYPE):
        """Start lobby countdown timer"""
        self.lobby_start_time = datetime.now()
        logger.info(f"Lobby timer started: {self.lobby_timeout} seconds")
        
        # Cancel existing timer if any
        if self.timer_task and not self.timer_task.done():
            self.timer_task.cancel()
        
        # Create new timer task
        self.timer_task = asyncio.create_task(
            self._run_lobby_timer(context)
        )
    
    async def _run_lobby_timer(self, context: ContextTypes.DEFAULT_TYPE):
        """Run the lobby timer and update message every 5 seconds"""
        try:
            update_interval = 5  # Update every 5 seconds
            elapsed = 0
            
            while elapsed < self.lobby_timeout:
                await asyncio.sleep(update_interval)
                elapsed += update_interval
                
                # Update lobby message
                try:
                    players = await db_manager.get_lobby_players()
                    lobby_message = await self.create_lobby_message(players=players)
                    
                    await context.bot.edit_message_text(
                        chat_id=self.lobby_chat_id,
                        message_id=self.lobby_message_id,
                        text=lobby_message,
                        reply_markup=self.get_lobby_keyboard()
                    )
                except BadRequest as e:
                    # Ignore "message not modified" errors (content unchanged)
                    if "message is not modified" in str(e).lower():
                        logger.debug(f"Lobby message unchanged, skipping update")
                    else:
                        logger.warning(f"BadRequest updating lobby timer: {e}")
                except Exception as e:
                    logger.error(f"Error updating lobby timer: {e}")
            
            # Timer expired - start game if minimum players reached
            logger.info("Lobby timer expired - checking if game can start")
            await self._handle_timer_expiry(context)
            
        except asyncio.CancelledError:
            logger.info("Lobby timer cancelled")
        except Exception as e:
            logger.error(f"Error in lobby timer: {e}")
    
    async def _handle_timer_expiry(self, context: ContextTypes.DEFAULT_TYPE):
        """Handle what happens when lobby timer expires"""
        players = await db_manager.get_lobby_players()
        count = len(players)
        
        logger.info(f"Timer expired with {count} players")
        
        if count < self.min_players:
            # Not enough players
            message = f"""⏱️ **LOBBY TIMEOUT**

❌ Player အရေအတွက် မလုံလောက်ပါ!

လက်ရှိ: {count} ယောက်
အနည်းဆုံး: {self.min_players} ယောက်

Game ကို စတင်၍ မရပါ။ နောက်တစ်ကြိမ် ထပ်စမ်းကြည့်ပါ။"""
            
            await context.bot.edit_message_text(
                chat_id=self.lobby_chat_id,
                message_id=self.lobby_message_id,
                text=message
            )
            
            # Clear lobby
            await db_manager.clear_lobby()
            return False
        
        # Remove excess players to form complete teams
        excess = count % config.TEAM_SIZE
        if excess > 0:
            logger.info(f"Removing {excess} excess players to form complete teams")
            
            # Get players sorted by join time (oldest first)
            sorted_players = sorted(players, key=lambda p: p.get('joined_at', ''))
            
            # Remove latest joiners (excess players)
            removed_players = sorted_players[-excess:]
            for player in removed_players:
                await db_manager.remove_from_lobby(player['user_id'])
                logger.info(f"Removed excess player: {player.get('username', 'Unknown')}")
            
            # Get final player list
            final_players = await db_manager.get_lobby_players()
            final_count = len(final_players)
            
            # Notify removed players
            for player in removed_players:
                try:
                    await context.bot.send_message(
                        chat_id=player['user_id'],
                        text=f"⚠️ **Lobby Full**\n\n"
                             f"Timer ပြီးဆုံးချိန်တွင် player များ ပြည့်လွန်းနေသောကြောင့် "
                             f"သင့်ကို lobby မှ ဖယ်ရှားခဲ့ရပါသည်။\n\n"
                             f"နောက်တစ်ကြိမ် ထပ်စမ်းကြည့်ပါ!"
                    )
                except Exception as e:
                    logger.error(f"Error notifying removed player {player['user_id']}: {e}")
            
            logger.info(f"Final player count after removal: {final_count}")
        
        # Start game
        num_teams = count // config.TEAM_SIZE
        message = f"""⏱️ **TIMER EXPIRED - GAME STARTING**

✅ Players: {len(await db_manager.get_lobby_players())} ယောက်
🏆 Teams: {num_teams} teams

⏳ Game ကို စတင်နေပါပြီ..."""
        
        try:
            await context.bot.edit_message_text(
                chat_id=self.lobby_chat_id,
                message_id=self.lobby_message_id,
                text=message
            )
        except Exception as e:
            logger.error(f"Error updating start message: {e}")
        
        # Trigger game start
        from handlers.game_handler import game_handler
        await game_handler.start_game(context, self.lobby_chat_id, self.lobby_message_id)
        
        return True
    
    def cancel_lobby_timer(self):
        """Cancel the lobby timer"""
        if self.timer_task and not self.timer_task.done():
            self.timer_task.cancel()
            logger.info("Lobby timer cancelled")
        
        self.lobby_start_time = None
        self.lobby_chat_id = None
        self.lobby_message_id = None
    
    async def handle_join(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
        """Handle player joining lobby
        
        Returns:
            True if max players reached and game should start immediately
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
        
        # Check if lobby is already full
        count = await db_manager.get_lobby_count()
        if count >= self.max_players:
            logger.warning(f"User {user_id} tried to join but lobby is full ({count}/{self.max_players})")
            await query.answer(
                f"⚠️ Lobby ပြည့်ပြီးပါပြီ! ({count}/{self.max_players})\n\n"
                "နောက်တစ်ကြိမ် ထပ်စမ်းကြည့်ပါ။",
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
        
        # Longer delay to avoid rate limiting when multiple joins happen quickly
        # Especially important for 12-15 player games
        await asyncio.sleep(0.6)
        
        # Test if bot can send private messages to user
        try:
            test_message = await context.bot.send_message(
                chat_id=user_id,
                text="✅ သင် lobby သို့ အောင်မြင်စွာ ဝင်ရောက်ပြီးပါပြီ!\n\n"
                     "Game စတင်ပြီး voting messages များကို ဒီမှာ ရရှိမှာပါ။"
            )
            logger.debug(f"Private message test successful for user {user_id}")
        except Exception as e:
            # Can't send private message - remove from lobby
            logger.warning(f"Cannot send private message to user {user_id}: {e}")
            await db_manager.remove_from_lobby(user_id)
            
            await query.answer(
                "⚠️ Bot ကို အရင် စတင်ပေးရပါမယ်!\n\n"
                "1️⃣ Bot ကို private chat မှာ /start နှိပ်ပါ\n"
                "2️⃣ ပြီးရင် ပြန်လာပြီး Join နှိပ်ပါ",
                show_alert=True
            )
            return False
        
        # Get current count after successful join
        new_count = await db_manager.get_lobby_count()
        
        # Start timer if this is the first player
        if new_count == 1:
            self.lobby_chat_id = query.message.chat_id
            self.lobby_message_id = query.message.message_id
            await self.start_lobby_timer(context)
            logger.info("First player joined - lobby timer started")
        
        # Update message
        lobby_message = await self.create_lobby_message(update)
        await query.edit_message_text(
            text=lobby_message,
            reply_markup=self.get_lobby_keyboard()
        )
        
        # Check if we reached max players (immediate start)
        if new_count >= self.max_players:
            logger.info(f"Max players reached ({new_count}/{self.max_players})! Starting game immediately")
            self.cancel_lobby_timer()
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


