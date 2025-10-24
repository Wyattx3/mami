"""
Main Telegram Bot Entry Point
"""
import logging
import asyncio
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler, 
    CallbackQueryHandler, 
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)

import config

# Initialize structured logging first
from utils.logger_config import init_logging
init_logging(level=config.LOG_LEVEL, enable_console=config.ENABLE_CONSOLE_LOGS)

# Reduce noise from third-party libraries in production
if config.LOG_LEVEL in ['WARNING', 'ERROR', 'CRITICAL']:
    logging.getLogger('telegram').setLevel(logging.ERROR)
    logging.getLogger('telegram.ext').setLevel(logging.ERROR)
    logging.getLogger('httpx').setLevel(logging.ERROR)
    logging.getLogger('asyncio').setLevel(logging.ERROR)

# Keep alive for Replit (prevents sleeping on free tier)
if os.getenv('REPLIT_DEPLOYMENT'):
    try:
        from keep_alive import keep_alive
        keep_alive()
        logging.info("Keep alive server started for Replit")
    except ImportError:
        logging.warning("Keep alive module not found, skipping")

from database.db_manager import db_manager
from handlers.lobby_handler import lobby_handler
from handlers.game_handler import game_handler
from handlers.voting_handler import voting_handler
from utils.helpers import get_team_name
from models.character import Character
from utils.constants import MBTI_TYPES, ZODIAC_SIGNS

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states for character addition
CHAR_NAME, CHAR_MBTI, CHAR_ZODIAC, CHAR_PASSWORD = range(4)

# Admin passwords
ADMIN_PASSWORDS = ["Wyatt#9810", "Yuyalay2000"]


# ==================== Command Handlers ====================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    logger.info(f"User {update.effective_user.id} ({update.effective_user.username}) used /start")
    
    # Check if private chat or group chat
    from telegram.constants import ChatType
    chat_type = update.message.chat.type
    
    if chat_type == ChatType.PRIVATE:
        # Private chat - Show "Add to Group" and "Help" buttons
        logger.debug(f"Private chat detected for user {update.effective_user.id}")
        welcome_message = """
🎮 **Telegram Strategy Game**

MBTI နှင့် Zodiac signs ကို အခြေခံထားတဲ့ team-based strategy game ကြိုဆိုပါတယ်!

**Game Rules:**
• 9 players, 3 teams (3 players each)
• 5 rounds of voting
• AI-based character-role matching
• Best team wins!

🎯 **Game ကစားချင်ရင် group chat မှာ ထည့်ပြီး စတင်ပါ!**
"""
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add to Group", url=f"https://t.me/{context.bot.username}?startgroup=true")],
            [InlineKeyboardButton("❓ Help", callback_data="show_help")]
        ])
        await update.message.reply_text(welcome_message, reply_markup=keyboard, parse_mode='Markdown')
    
    else:
        # Group/Supergroup chat
        logger.debug(f"Group chat detected: {update.message.chat.title}")
        
        # Check if channel already has an active game
        chat_id = update.message.chat_id
        has_active_game = await db_manager.is_channel_has_active_game(chat_id)
        
        if has_active_game:
            # Active game exists - don't show New Game button
            logger.warning(f"Channel {chat_id} already has active game, not showing New Game button")
            welcome_message = """
🎮 **Telegram Strategy Game**

MBTI နှင့် Zodiac signs ကို အခြေခံထားတဲ့ team-based strategy game ကြိုဆိုပါတယ်!

⚠️ **ဒီ group မှာ game တခု စနေပါပြီ!**

Game ပြီးမှ `/start` ကို ထပ်ပို့ပြီး game အသစ်စတင်နိုင်ပါတယ်။
"""
            await update.message.reply_text(welcome_message, parse_mode='Markdown')
        else:
            # No active game - show New Game button
            welcome_message = """
🎮 **Telegram Strategy Game**

MBTI နှင့် Zodiac signs ကို အခြေခံထားတဲ့ team-based strategy game ကြိုဆိုပါတယ်!

**Game Rules:**
• 9 players, 3 teams (3 players each)
• 5 rounds of voting
• AI-based character-role matching
• Best team wins!

Ready to play? 🎉
"""
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🎮 New Game", callback_data="start_newgame")]
            ])
            await update.message.reply_text(welcome_message, reply_markup=keyboard, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    logger.info(f"User {update.effective_user.id} used /help")
    
    help_text = """
📚 **အကူအညီ & လမ်းညွှန်**

Game ကစားနည်း၊ rules နှင့် features များကို အသေးစိတ် သိရှိနိုင်ပါတယ်။

အောက်က ခလုတ်များကို နှိပ်ပြီး လေ့လာပါ:
"""
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 ဘယ်လို စတင်မလဲ?", callback_data="help_start")],
        [InlineKeyboardButton("📜 Game Rules", callback_data="help_rules")],
        [InlineKeyboardButton("🗳️ Voting System", callback_data="help_voting")],
        [InlineKeyboardButton("👑 Roles & Characters", callback_data="help_roles")],
        [InlineKeyboardButton("🏆 Scoring System", callback_data="help_scoring")],
        [InlineKeyboardButton("⚙️ Commands", callback_data="help_commands")],
        [InlineKeyboardButton("❓ FAQ", callback_data="help_faq")],
    ])
    
    await update.message.reply_text(help_text, reply_markup=keyboard, parse_mode='Markdown')


async def newgame_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /newgame command"""
    logger.info(f"User {update.effective_user.id} ({update.effective_user.username}) tried to create new game")
    
    # Check if private chat or group chat
    from telegram.constants import ChatType
    chat_type = update.message.chat.type
    
    if chat_type == ChatType.PRIVATE:
        # Private chat - Show "Add to Group" button
        logger.warning(f"User {update.effective_user.id} tried to start game in private chat")
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Bot to Group", url=f"https://t.me/{context.bot.username}?startgroup=true")],
            [InlineKeyboardButton("❓ Help", callback_data="show_help")]
        ])
        await update.message.reply_text(
            "⚠️ **Game ကို group chat မှာသာ စတင်နိုင်ပါတယ်!**\n\n"
            "Bot ကို သင့် group မှာ ထည့်ပြီး `/newgame` ကို ထပ်စမ်းကြည့်ပါ။",
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
        return
    
    # Group chat - Continue with normal game creation
    logger.info(f"New game attempt in group: {update.message.chat.title}")
    
    # Check if channel already has an active game
    chat_id = update.message.chat_id
    has_active_game = await db_manager.is_channel_has_active_game(chat_id)
    if has_active_game:
        logger.warning(f"Channel {chat_id} already has an active game")
        await update.message.reply_text(
            "⚠️ **ဒီ group မှာ game တခု ပွဲစနေပါပြီ!**\n\n"
            "Game တပွဲပြီးမှ နောက်တပွဲ စနိုင်ပါမယ်။",
            parse_mode='Markdown'
        )
        return
    
    # Check if lobby is already open (players waiting to join)
    lobby_count = await db_manager.get_lobby_count()
    if lobby_count > 0:
        logger.warning(f"Channel {chat_id} already has an active lobby with {lobby_count} players")
        await update.message.reply_text(
            f"⚠️ **Lobby တစ်ခု ဖွင့်ထားပြီးသားပါ!**\n\n"
            f"လက်ရှိ players: {lobby_count}\n\n"
            f"အဲဒီ lobby မှာ join လုပ်ပါ သို့မဟုတ် lobby ပိတ်သွားသည့်အထိ စောင့်ပါ။",
            parse_mode='Markdown'
        )
        return
    
    logger.info(f"New game created in group: {update.message.chat.title}")
    
    # Check if enough characters
    char_count = await db_manager.get_character_count()
    min_required = config.CHARACTERS_PER_VOTING * 3  # At least 3 rounds worth
    
    if char_count < min_required:
        logger.warning(f"Not enough characters for game: {char_count}/{min_required}")
        await update.message.reply_text(
            f"⚠️ Database မှာ character အရေအတွက် မလုံလောက်ပါ!\n\n"
            f"လက်ရှိ: {char_count}\nလိုအပ်သည်: {min_required}\n\n"
            f"`/addcharacter` သုံးပြီး characters ထည့်ပါ။",
            parse_mode='Markdown'
        )
        return
    
    # Create lobby message
    lobby_message = await lobby_handler.create_lobby_message(update)
    keyboard = lobby_handler.get_lobby_keyboard()
    
    message = await update.message.reply_text(
        lobby_message,
        reply_markup=keyboard,
        parse_mode='Markdown'
    )
    
    # Store message info for later use
    context.user_data['lobby_message_id'] = message.message_id
    context.user_data['lobby_chat_id'] = message.chat_id


async def cancelgame_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /cancelgame command - cancel active game"""
    import aiosqlite
    from telegram.constants import ChatType
    from utils.constants import GAME_STATUS
    
    logger.info(f"User {update.effective_user.id} ({update.effective_user.username}) tried to cancel game")
    
    # Check if private chat or group chat
    chat_type = update.message.chat.type
    
    if chat_type == ChatType.PRIVATE:
        logger.warning(f"User {update.effective_user.id} tried to cancel game in private chat")
        await update.message.reply_text(
            "⚠️ **Game ကို group chat မှာသာ cancel လုပ်နိုင်ပါတယ်!**",
            parse_mode='Markdown'
        )
        return
    
    # Check if channel has an active game
    chat_id = update.message.chat_id
    has_active_game = await db_manager.is_channel_has_active_game(chat_id)
    
    if not has_active_game:
        logger.warning(f"Channel {chat_id} has no active game to cancel")
        await update.message.reply_text(
            "⚠️ **ဒီ group မှာ cancel လုပ်ဖို့ game မရှိပါ!**\n\n"
            "Active game တခု ရှိမှသာ cancel လုပ်နိုင်ပါမယ်။",
            parse_mode='Markdown'
        )
        return
    
    # Get active game details
    async with aiosqlite.connect(db_manager.db_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            'SELECT id, status FROM games WHERE lobby_chat_id = ? AND status IN (?, ?) ORDER BY id DESC LIMIT 1',
            (chat_id, GAME_STATUS['LOBBY'], GAME_STATUS['IN_PROGRESS'])
        )
        game_row = await cursor.fetchone()
    
    if not game_row:
        logger.error(f"Channel {chat_id} - Active game check passed but no game found")
        await update.message.reply_text(
            "❌ **Error: Game ကို ရှာမတွေ့ပါ!**",
            parse_mode='Markdown'
        )
        return
    
    game_id = game_row['id']
    game_status = game_row['status']
    
    # Permission check - group admins or game participants can cancel
    user_id = update.effective_user.id
    
    # Check if user is group admin
    chat_member = await context.bot.get_chat_member(chat_id, user_id)
    is_admin = chat_member.status in ['creator', 'administrator']
    
    # Check if user is in the game
    is_participant = await db_manager.is_user_in_game(game_id, user_id)
    
    if not (is_admin or is_participant):
        logger.warning(f"User {user_id} tried to cancel game {game_id} without permission")
        await update.message.reply_text(
            "⚠️ **Game ကို cancel လုပ်ခွင့် မရှိပါ!**\n\n"
            "Group admin သို့မဟုတ် game မှာ ပါဝင်နေသူများသာ cancel လုပ်နိုင်ပါတယ်။",
            parse_mode='Markdown'
        )
        return
    
    # Cancel the game
    logger.info(f"Cancelling game {game_id} (status: {game_status}) by user {user_id}")
    
    # Update game status to cancelled
    await db_manager.update_game_status(game_id, GAME_STATUS['CANCELLED'])
    
    # Cleanup game data
    if game_id in voting_handler.active_votes:
        del voting_handler.active_votes[game_id]
        logger.debug(f"Cleared votes for game {game_id}")
    
    if game_id in voting_handler.voting_messages:
        del voting_handler.voting_messages[game_id]
        logger.debug(f"Cleared voting messages for game {game_id}")
    
    if game_id in voting_handler.round_timers:
        del voting_handler.round_timers[game_id]
        logger.debug(f"Cleared round timers for game {game_id}")
    
    # Clear player teams
    players_to_remove = [uid for uid, data in game_handler.player_teams.items() 
                        if data['game_id'] == game_id]
    for uid in players_to_remove:
        del game_handler.player_teams[uid]
    logger.debug(f"Cleared team info for {len(players_to_remove)} players")
    
    # Clear active game
    if game_id in game_handler.active_games:
        del game_handler.active_games[game_id]
        logger.debug(f"Removed game {game_id} from active games")
    
    # Clear lobby queue if in lobby state
    if game_status == GAME_STATUS['LOBBY']:
        await lobby_handler.clear_lobby(chat_id)
        logger.debug(f"Cleared lobby queue for chat {chat_id}")
    
    # Announce cancellation
    username = update.effective_user.username or update.effective_user.first_name or f"User_{user_id}"
    status_text = "Lobby" if game_status == GAME_STATUS['LOBBY'] else "Game"
    
    await update.message.reply_text(
        f"🚫 **{status_text} ကို cancel လုပ်ပြီးပါပြီ!**\n\n"
        f"Cancelled by: @{username}\n\n"
        f"Game အသစ် စတင်ချင်ရင် `/newgame` သုံးပါ။",
        parse_mode='Markdown'
    )
    
    logger.info(f"Game {game_id} cancelled successfully by user {user_id}")


# ==================== Character Addition (Conversation) ====================

async def addcharacter_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start character addition conversation"""
    logger.info(f"User {update.effective_user.id} started /addcharacter")
    await update.message.reply_text(
        "✏️ **Character အသစ် ထည့်ရန်**\n\n"
        "Character name ကို ရိုက်ထည့်ပါ (English letters only):",
        parse_mode='Markdown'
    )
    return CHAR_NAME


async def char_name_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive character name"""
    name = update.message.text.strip()
    logger.debug(f"User {update.effective_user.id} entered character name: {name}")
    
    # Validate English letters only (allow spaces)
    if not all(c.isalpha() or c.isspace() for c in name):
        logger.warning(f"Invalid character name (non-English): {name}")
        await update.message.reply_text(
            "❌ Character name မှာ English letters သာ ပါရပါမယ်!\n\n"
            "ထပ်မံ ကြိုးစားပါ:",
            parse_mode='Markdown'
        )
        return CHAR_NAME
    
    context.user_data['char_name'] = name
    
    # Create MBTI selection buttons (4x4 grid)
    keyboard = []
    for i in range(0, len(MBTI_TYPES), 4):
        row = [
            InlineKeyboardButton(mbti, callback_data=f"mbti_{mbti}")
            for mbti in MBTI_TYPES[i:i+4]
        ]
        keyboard.append(row)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"✅ Name: **{name}**\n\n"
        f"MBTI type ကို ရွေးချယ်ပါ:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return CHAR_MBTI


async def char_mbti_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive character MBTI from button"""
    query = update.callback_query
    await query.answer()
    
    # Parse MBTI from callback data
    mbti = query.data.replace('mbti_', '')
    logger.debug(f"User {query.from_user.id} selected MBTI: {mbti}")
    
    if mbti not in MBTI_TYPES:
        await query.edit_message_text("❌ Invalid MBTI type!")
        return CHAR_MBTI
    
    context.user_data['char_mbti'] = mbti
    
    # Create Zodiac selection buttons (3x4 grid)
    keyboard = []
    for i in range(0, len(ZODIAC_SIGNS), 3):
        row = [
            InlineKeyboardButton(zodiac, callback_data=f"zodiac_{zodiac}")
            for zodiac in ZODIAC_SIGNS[i:i+3]
        ]
        keyboard.append(row)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"✅ Name: **{context.user_data['char_name']}**\n"
        f"✅ MBTI: **{mbti}**\n\n"
        f"Zodiac sign ကို ရွေးချယ်ပါ:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return CHAR_ZODIAC


async def char_zodiac_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive character zodiac from button"""
    query = update.callback_query
    await query.answer()
    
    # Parse zodiac from callback data
    zodiac = query.data.replace('zodiac_', '')
    logger.debug(f"User {query.from_user.id} selected zodiac: {zodiac}")
    
    if zodiac not in ZODIAC_SIGNS:
        await query.edit_message_text("❌ Invalid zodiac sign!")
        return CHAR_ZODIAC
    
    context.user_data['char_zodiac'] = zodiac
    
    # Generate description using AI
    await query.edit_message_text(
        f"✅ Name: **{context.user_data['char_name']}**\n"
        f"✅ MBTI: **{context.user_data['char_mbti']}**\n"
        f"✅ Zodiac: **{zodiac}**\n\n"
        f"⏳ AI က description ရေးနေပါသည်...",
        parse_mode='Markdown'
    )
    
    # Generate AI description
    from services.ai_service import ai_service
    from models.character import Character
    
    temp_character = Character(
        id=None,
        name=context.user_data['char_name'],
        mbti=context.user_data['char_mbti'],
        zodiac=zodiac,
        description=""
    )
    
    description = await ai_service.generate_character_description(temp_character)
    context.user_data['char_description'] = description
    
    # Ask for admin password
    await query.message.reply_text(
        f"✅ Name: **{context.user_data['char_name']}**\n"
        f"✅ MBTI: **{context.user_data['char_mbti']}**\n"
        f"✅ Zodiac: **{zodiac}**\n"
        f"✅ Description: {description}\n\n"
        f"🔐 Admin password ကို ရိုက်ထည့်ပါ:",
        parse_mode='Markdown'
    )
    
    return CHAR_PASSWORD


async def char_password_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive admin password and save character"""
    password = update.message.text.strip()
    user_id = update.effective_user.id
    logger.debug(f"User {user_id} entered admin password")
    
    # Verify admin password
    if password not in ADMIN_PASSWORDS:
        logger.warning(f"User {user_id} entered incorrect admin password: {password}")
        await update.message.reply_text(
            "❌ **Admin password မှားနေပါတယ်!**\n\n"
            "Character ကို မထည့်နိုင်ပါ။ Process ကို cancel လုပ်လိုက်ပါပြီ။\n\n"
            "ထပ်မံ ကြိုးစားချင်ရင် `/addcharacter` command ကို ထပ်ပို့ပါ။",
            parse_mode='Markdown'
        )
        context.user_data.clear()
        return ConversationHandler.END
    
    # Create character
    character = Character(
        id=None,
        name=context.user_data['char_name'],
        mbti=context.user_data['char_mbti'],
        zodiac=context.user_data['char_zodiac'],
        description=context.user_data['char_description']
    )
    
    # Save to database
    try:
        char_id = await db_manager.add_character(character)
        logger.info(f"User {user_id} successfully added character: {character.name} (ID: {char_id})")
        
        await update.message.reply_text(
            f"✅ **Character ထည့်ပြီးပါပြီ!**\n\n"
            f"**ID:** {char_id}\n"
            f"**Name:** {character.name}\n"
            f"**MBTI:** {character.mbti}\n"
            f"**Zodiac:** {character.zodiac}\n"
            f"**Description:** {character.description}",
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error adding character: {e}")
        await update.message.reply_text(
            f"❌ **Error:** {str(e)}\n\n"
            f"Character name က ထပ်နေမလား စစ်ကြည့်ပါ။"
        )
    
    # Clear user data
    context.user_data.clear()
    
    return ConversationHandler.END


async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel conversation"""
    await update.message.reply_text("❌ Cancelled.")
    context.user_data.clear()
    return ConversationHandler.END


# ==================== Callback Handlers ====================

async def lobby_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle lobby join/quit callbacks"""
    query = update.callback_query
    logger.debug(f"Lobby callback: {query.data} from user {query.from_user.id}")
    
    if query.data == "join_lobby":
        is_full = await lobby_handler.handle_join(update, context)
        
        if is_full:
            # Announce game start
            await lobby_handler.announce_game_start(
                context, 
                query.message.chat_id, 
                query.message.message_id
            )
            
            # Start game in background
            asyncio.create_task(
                game_handler.start_game(
                    context,
                    query.message.chat_id,
                    query.message.message_id
                )
            )
    
    elif query.data == "quit_lobby":
        await lobby_handler.handle_quit(update, context)


async def vote_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle vote callbacks"""
    await voting_handler.handle_vote(update, context)


async def details_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle details button callback"""
    query = update.callback_query
    await query.answer()
    
    # Parse callback_data: details_{game_id}_{team_id}
    parts = query.data.split('_')
    if len(parts) != 3:
        await query.answer("Invalid request", show_alert=True)
        return
    
    game_id = int(parts[1])
    team_id = int(parts[2])
    
    logger.info(f"Details requested for game {game_id}, team {team_id}")
    
    # Get detailed explanations from database
    game_rounds = await db_manager.get_game_rounds(game_id)
    
    # Filter rounds for this team
    team_rounds = [r for r in game_rounds if r.team_id == team_id]
    
    if not team_rounds:
        await query.answer("No data found", show_alert=True)
        return
    
    # Build explanation message
    from utils.helpers import get_team_name
    
    # Get team name
    team_players = []
    # Get team players from game_players table
    teams = await db_manager.get_game_players(game_id)
    team_players = teams.get(team_id, [])
    
    team_name = get_team_name(team_players) if team_players else f"Team {team_id}"
    
    lines = [f"📊 **{team_name} - Detailed Explanations**\n"]
    
    for game_round in team_rounds:
        if game_round.selected_character_id:
            character = await db_manager.get_character(game_round.selected_character_id)
            if character:
                role_name = game_round.role
                score = game_round.score or 0
                explanation = game_round.explanation or "No explanation available"
                
                lines.append(f"**{role_name}: {character.name}**")
                lines.append(f"Score: {score}/10")
                lines.append(f"Explanation: {explanation}\n")
    
    explanation_message = "\n".join(lines)
    
    # Edit the message with back button
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data=f"back_{game_id}_{team_id}")]
    ])
    
    try:
        await query.edit_message_text(
            text=explanation_message,
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
        logger.debug(f"Edited message with details for team {team_id}")
    except Exception as e:
        logger.error(f"Error editing message with details: {e}")
        await query.answer("Error showing details", show_alert=True)


async def show_main_help_menu(query):
    """Show main help menu with sections"""
    help_text = """
📚 **အကူအညီ & လမ်းညွှန်**

Game ကစားနည်း၊ rules နှင့် features များကို အသေးစိတ် သိရှိနိုင်ပါတယ်။

အောက်က ခလုတ်များကို နှိပ်ပြီး လေ့လာပါ:
"""
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 ဘယ်လို စတင်မလဲ?", callback_data="help_start")],
        [InlineKeyboardButton("📜 Game Rules", callback_data="help_rules")],
        [InlineKeyboardButton("🗳️ Voting System", callback_data="help_voting")],
        [InlineKeyboardButton("👑 Roles & Characters", callback_data="help_roles")],
        [InlineKeyboardButton("🏆 Scoring System", callback_data="help_scoring")],
        [InlineKeyboardButton("⚙️ Commands", callback_data="help_commands")],
        [InlineKeyboardButton("❓ FAQ", callback_data="help_faq")],
    ])
    
    await query.edit_message_text(help_text, reply_markup=keyboard, parse_mode='Markdown')


async def show_detailed_help(query, help_type):
    """Show detailed help page based on type"""
    help_pages = {
        "help_start": {
            "title": "🎮 ဘယ်လို စတင်မလဲ?",
            "content": """
**Setup လုပ်ခြင်း:**

1️⃣ Bot ကို သင့် group chat မှာ ထည့်ပါ
   • Admin permissions ပေးပါ
   • Members အများကြီး invite လုပ်ပါ (အနည်းဆုံး 9 ယောက်)

2️⃣ Game စတင်ခြင်း:
   • `/newgame` command ပို့ပါ
   • Lobby ပေါ်လာမယ်

3️⃣ Players ဝင်ရောက်ခြင်း:
   • "Join Game" button ကို နှိပ်ပါ
   • 9 players ပြည့်ရင် game စတင်ပါမယ်

4️⃣ Team Formation:
   • Game က automatically 3 teams ခွဲပါမယ်
   • Team တခုမှာ 3 players ရှိပါမယ်
   • Team leader ကို random ရွေးပါမယ်

5️⃣ Voting Rounds:
   • 5 rounds ရှိပါမယ်
   • Round တိုင်းမှာ character 4 ခု ပြပါမယ်
   • Team chat နှင့် private chat မှာ vote လုပ်နိုင်ပါတယ်

6️⃣ Results:
   • Round ပြီးတိုင်း ရလဒ် ပြပါမယ်
   • Game ပြီးရင် winner team ကြေညာပါမယ်

**Tips:**
✅ Internet connection ကောင်းကောင်း ရှိပါစေ
✅ Private chat မှာ bot ကို start လုပ်ထားပါ
✅ Team members တွေနဲ့ ညှိနှိုင်းဖို့ အဆင်သင့်ပါ
"""
        },
        "help_rules": {
            "title": "📜 Game Rules",
            "content": """
**အခြေခံ Rules:**

👥 **Players:**
   • Total: 9 players
   • Teams: 3 teams (3 players each)
   • Leader: Team တခုစီမှာ 1 leader

⏱️ **Time Limits:**
   • Voting: 60-120 seconds per round
   • Discussion: Team chat မှာ အချိန်မရှိ

🎯 **Rounds:**
   • Total: 5 rounds
   • Each round has a specific role
   • Characters နှင့် roles ကို AI က match လုပ်ပါမယ်

🏆 **Winning:**
   • Highest total score wins
   • AI က character-role matching ကို score လုပ်ပါမယ်
   • Perfect match = 10 points
   • Good match = 7 points
   • Average match = 5 points
   • Poor match = 3 points

⚖️ **Fairness:**
   • Character reuse: Round 3 ခု ပြီးမှသာ ထပ်သုံးနိုင်ပါတယ်
   • Random team formation
   • AI-based objective scoring
   • All players vote simultaneously

❌ **Restrictions:**
   • Late votes are rejected
   • One vote per player per round
   • Cannot change vote after submission
   • Game တပွဲစီ သီးခြားလုံးဝ သီးခြားဖြစ်ပါမယ်
"""
        },
        "help_voting": {
            "title": "🗳️ Voting System",
            "content": """
**Vote လုပ်နည်း:**

📋 **Character Selection:**
   • Round တိုင်းမှာ character 4 ခု ပြပါမယ်
   • သင့် team ရဲ့ အလှည့်ဆိုရင် vote လုပ်နိုင်ပါတယ်
   • တခုတည်းသာ ရွေးချယ်နိုင်ပါတယ်

🗨️ **Voting Locations:**
   • **Team Chat:** Team members တွေ မြင်ပါမယ်
   • **Private Chat:** Bot က သင့်ကို message ပို့ပါမယ်

⚡ **Real-time Updates:**
   • Vote လုပ်တာနဲ့ team members တွေ သိပါမယ်
   • "X voted for Y" notification ရပါမယ်
   • Vote count real-time update ဖြစ်ပါမယ်

🎲 **Vote Resolution:**

**Case 1: Clear Majority (e.g., 2:1 or 3:0)**
   ✅ Most voted character wins

**Case 2: Leader vs Others (1:1:1)**
   👑 Leader's vote wins
   • Team leader ရဲ့ vote က priority ရှိပါတယ်

**Case 3: Tie without Leader (1:1, no leader)**
   ⏰ First voter wins
   • အရင်ဆုံး vote လုပ်သူရဲ့ choice က win ပါမယ်

**Case 4: All Different (1:1:1 with leader)**
   👑 Leader's vote wins

⏱️ **Time Management:**
   • Vote လုပ်ဖို့ 60-120 seconds
   • Time ကုန်ရင် မဲမထည့်သေးသူတွေ random ရွေးပါမယ်
   • Late votes are rejected

✅ **Confirmation:**
   • Vote လုပ်ပြီးရင် confirmation message ရပါမယ်
   • Role name နှင့် character name ပြပါမယ်
   • Vote ပြောင်းလို့ မရပါဘူး
"""
        },
        "help_roles": {
            "title": "👑 Roles & Characters",
            "content": """
**5 Rounds, 5 Roles:**

**Round 1: 👑 ဘုရင် (King/Queen)**
   • လိုအပ်သော စွမ်းရည်များ:
     - Leadership
     - Decision making
     - Strategic thinking

**Round 2: ⚔️ စစ်သူကြီး (General)**
   • လိုအပ်သော စွမ်းရည်များ:
     - Courage
     - Tactical skills
     - Quick decision

**Round 3: 🧠 အကြံပေး (Advisor)**
   • လိုအပ်သော စွမ်းရည်များ:
     - Wisdom
     - Analysis
     - Problem solving

**Round 4: 🌾 လယ်သမား (Farmer)**
   • လိုအပ်သော စွမ်းရည်များ:
     - Resource management
     - Hard work
     - Practicality

**Round 5: 🙏 ဘုန်းကြီး (Monk)**
   • လိုအပ်သော စွမ်းရည်များ:
     - Wisdom
     - Calmness
     - Diplomacy

**Character System:**
   • MBTI: 16 personality types
   • Zodiac: 12 astrological signs
   • AI က MBTI + Zodiac သုံးပြီး role နှင့် match လုပ်ပါမယ်
   • Character description တွေလည်း ထည့်တွက်ပါတယ်
   • ဘယ် character က ဘယ် role နဲ့ ကိုက်မယ်ဆိုတာ AI က သီးခြားစီ analyze လုပ်ပါမယ်

**Character Reuse:**
   • Same character: Round 3 ခု ကြာမှ ထပ်သုံးနိုင်ပါတယ်
   • ဒါကြောင့် variety ရှိပါမယ်
   • Database မှာ character အများကြီး ရှိပါတယ်
"""
        },
        "help_scoring": {
            "title": "🏆 Scoring System",
            "content": """
**AI-based Scoring:**

🤖 **Google Gemini AI:**
   • Character profiles ကို analyze လုပ်ပါမယ်
   • MBTI နှင့် Zodiac compatibility စစ်ပါမယ်
   • Role requirements နှင့် match လုပ်ပါမယ်

📊 **Score Distribution:**

**Perfect Match (10 points):**
   ✅ MBTI perfectly suits role
   ✅ Zodiac strongly supports role
   ✅ Character traits align 100%

**Good Match (7 points):**
   ✅ MBTI suits role well
   ✅ Zodiac moderately supports
   ✅ Character traits align 70-90%

**Average Match (5 points):**
   ⚠️ MBTI somewhat suits role
   ⚠️ Zodiac neutral
   ⚠️ Character traits align 50-70%

**Poor Match (3 points):**
   ❌ MBTI doesn't suit role well
   ❌ Zodiac may conflict
   ❌ Character traits align <50%

**Minimum (1 point):**
   ❌ Complete mismatch
   ❌ AI couldn't find compatibility

💯 **Total Score:**
   • Each team: 5 rounds × 10 max = 50 points
   • Winner: Highest total score
   • Tie: Multiple winners possible

📈 **Scoring Factors:**
   1. MBTI-Role compatibility (40%)
   2. Zodiac-Role compatibility (30%)
   3. Character description analysis (20%)
   4. Overall synergy (10%)

🎯 **Strategy Tips:**
   • ဘာစီးရှည်စဉ်းစားပါ role requirements ကို
   • MBTI နှင့် Zodiac သိထားပါ
   • Team coordination အရေးကြီးပါတယ်
   • Leader ရဲ့ decision က အရေးကြီးပါတယ်
"""
        },
        "help_commands": {
            "title": "⚙️ Available Commands",
            "content": """
**Player Commands:**

`/start`
   • Bot ကို စတင်ပါ
   • Private chat: Welcome message
   • Group chat: New game option

`/newgame`
   • Game အသစ် ဖန်တီးပါ
   • Group chat မှာသာ သုံးနိုင်ပါတယ်
   • Lobby ပေါ်လာမယ်

`/help`
   • အကူအညီ menu ဖွင့်ပါ
   • အသေးစိတ် လမ်းညွှန်ချက်များ

`/cancelgame`
   • လက်ရှိ game ကို ဖျက်ပါ
   • Lobby stage မှာသာ သုံးနိုင်ပါတယ်
   • Game creator သာ ဖျက်နိုင်ပါတယ်

`/addcharacter`
   • Character အသစ် ထည့်ပါ
   • Admin password လိုအပ်ပါတယ်
   • Name, MBTI, Zodiac ထည့်ရပါမယ်

`/listcharacters`
   • Database မှာရှိတဲ့ characters တွေ ကြည့်ပါ
   • Total count ပြပါမယ်

**Button Actions:**

🎮 **Join Game**
   • Lobby မှာ game ဝင်ရန်

🚪 **Leave Game**
   • Lobby မှာ game ထွက်ရန်

🗳️ **Vote Buttons**
   • Character ရွေးချယ်ရန်

📊 **Details Button**
   • Round results အသေးစိတ် ကြည့်ရန်

🔙 **Back Button**
   • ပြန်သွားရန်

**Admin Features:**
   • Password protected
   • Character management
   • Game data access
"""
        },
        "help_faq": {
            "title": "❓ Frequently Asked Questions",
            "content": """
**Q: Bot ကို private chat မှာ စတင်ရမှာလား?**
A: မလိုပါဘူး။ Group chat မှာ တည့်ငေ `/newgame` ပို့နိုင်ပါတယ်။ ဒါပေမယ့် private messages ရဖို့ start လုပ်ထားသင့်ပါတယ်။

**Q: 9 players မပြည့်ရင် ဘာဖြစ်မလဲ?**
A: Game မစပါဘူး။ 9 players ပြည့်မှ game စပါမယ်။

**Q: Vote ပြောင်းလို့ရလား?**
A: မရပါဘူး။ Vote submit လုပ်ပြီးရင် ပြောင်းလို့မရတော့ပါ။

**Q: Time ကုန်ပြီး vote မလုပ်ရသေးရင်?**
A: System က random character ရွေးပေးပါမယ်။

**Q: Character များ ထပ်သုံးလို့ရလား?**
A: Round 3 ခု ကြာပြီးမှ ထပ်သုံးနိုင်ပါတယ်။

**Q: Team ကို ကိုယ်တိုင်ရွေးလို့ရလား?**
A: မရပါဘူး။ Random team formation ဖြစ်ပါတယ်။

**Q: AI scoring ကို ဘယ်လို အလုပ်လုပ်သလဲ?**
A: Google Gemini AI က MBTI, Zodiac နှင့် character traits ကို analyze လုပ်ပြီး role နှင့် match လုပ်ပါတယ်။

**Q: Game အလယ်မှာ ထွက်လို့ရလား?**
A: Lobby stage မှာသာ quit လုပ်လို့ရပါတယ်။ Game စပြီးရင် ထွက်လို့မရပါဘူး။

**Q: Private message မရရင်?**
A: Bot ကို private chat မှာ `/start` ပို့ပါ။ Bot ကို block မလုပ်ထားကြောင်း သေချာပါ။

**Q: ဘယ်လို character ထည့်မလဲ?**
A: `/addcharacter` သုံးပါ။ Admin password လိုအပ်ပါတယ်။

**Q: Error ဖြစ်ရင် ဘယ်လိုလုပ်မလဲ?**
A: `/cancelgame` နဲ့ game ဖျက်ပြီး ထပ်စမ်းကြည့်ပါ။ ဆက်မရရင် bot ကို restart လုပ်ပါ။

**Q: Score တူရင် ဘာဖြစ်မလဲ?**
A: Multiple winners ဖြစ်နိုင်ပါတယ်။ Both teams win ပါမယ်။

**ထပ်မံ မေးခွန်းများ ရှိရင် @cchrist3lle ကို ဆက်သွယ်ပါ။**
"""
        }
    }
    
    page = help_pages.get(help_type)
    if not page:
        await query.answer("Invalid help page", show_alert=True)
        return
    
    # Create back button
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Help Menu", callback_data="show_help")]
    ])
    
    full_text = f"**{page['title']}**\n{page['content']}"
    
    await query.edit_message_text(full_text, reply_markup=keyboard, parse_mode='Markdown')


async def help_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle help button callback"""
    query = update.callback_query
    await query.answer()
    
    # Check if it's detailed help page request
    if query.data.startswith("help_"):
        await show_detailed_help(query, query.data)
        return
    
    # Show main help menu
    await show_main_help_menu(query)


async def back_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle back button callback"""
    query = update.callback_query
    await query.answer()
    
    # Parse callback_data: back_{game_id}_{team_id}
    parts = query.data.split('_')
    if len(parts) != 3:
        await query.answer("Invalid request", show_alert=True)
        return
    
    game_id = int(parts[1])
    team_id = int(parts[2])
    
    logger.info(f"Back button pressed for game {game_id}, team {team_id}")
    
    # Get team results from database
    results = await db_manager.get_game_results(game_id)
    
    if team_id not in results:
        await query.answer("Team data not found", show_alert=True)
        return
    
    # Format the original results message
    from services.scoring_service import scoring_service
    from utils.helpers import get_team_name
    
    team_data = results[team_id]
    team_players = team_data.get('players', [])
    team_name = get_team_name(team_players) if team_players else f"Team {team_id}"
    
    # Get winner
    winner = max(results.keys(), key=lambda k: results[k]['total_score'])
    
    # Format message
    result_message = scoring_service.format_team_results(team_id, team_data)
    
    # Add winner indicator if this is winning team
    if team_id == winner:
        result_message = result_message.replace("Results**", "Results** 🏆")
    
    # Restore details button
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Details", callback_data=f"details_{game_id}_{team_id}")]
    ])
    
    try:
        await query.edit_message_text(
            text=result_message,
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
        logger.debug(f"Restored original results for team {team_id}")
    except Exception as e:
        logger.error(f"Error restoring results: {e}")
        await query.answer("Error going back", show_alert=True)


async def start_newgame_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle new game button callback from group chat"""
    query = update.callback_query
    await query.answer()
    
    logger.info(f"User {query.from_user.id} pressed New Game button in group")
    
    # Check if channel already has an active game
    chat_id = query.message.chat_id
    has_active_game = await db_manager.is_channel_has_active_game(chat_id)
    if has_active_game:
        logger.warning(f"Channel {chat_id} already has an active game")
        await query.edit_message_text(
            "⚠️ **ဒီ group မှာ game တခု ပွဲစနေပါပြီ!**\n\n"
            "Game တပွဲပြီးမှ နောက်တပွဲ စနိုင်ပါမယ်။",
            parse_mode='Markdown'
        )
        return
    
    # Check if lobby is already open
    lobby_count = await db_manager.get_lobby_count()
    if lobby_count > 0:
        logger.warning(f"Channel {chat_id} already has an active lobby with {lobby_count} players")
        await query.answer(
            f"⚠️ Lobby တစ်ခု ဖွင့်ထားပြီးသားပါ! ({lobby_count} players)\n\n"
            f"အဲဒီ lobby မှာ join လုပ်ပါ။",
            show_alert=True
        )
        return
    
    # Check if enough characters
    char_count = await db_manager.get_character_count()
    min_required = config.CHARACTERS_PER_VOTING * 3  # At least 3 rounds worth
    
    if char_count < min_required:
        logger.warning(f"Not enough characters for game: {char_count}/{min_required}")
        await query.edit_message_text(
            f"⚠️ Database မှာ character အရေအတွက် မလုံလောက်ပါ!\n\n"
            f"လက်ရှိ: {char_count}\nလိုအပ်သည်: {min_required}\n\n"
            f"`/addcharacter` သုံးပြီး characters ထည့်ပါ။",
            parse_mode='Markdown'
        )
        return
    
    # Create lobby
    lobby_message = f"""
🎮 **Game Lobby**

**Players:** 0/{config.LOBBY_SIZE}

Waiting for players to join...
"""
    keyboard = lobby_handler.get_lobby_keyboard()
    
    await query.edit_message_text(
        lobby_message,
        reply_markup=keyboard,
        parse_mode='Markdown'
    )
    
    # Store message info
    context.user_data['lobby_message_id'] = query.message.message_id
    context.user_data['lobby_chat_id'] = query.message.chat_id


# ==================== Team Chat Handler ====================

async def team_chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle team chat messages in private chat"""
    # Only handle private chat text messages
    if not update.message or not update.message.text:
        return
    
    from telegram.constants import ChatType
    if update.message.chat.type != ChatType.PRIVATE:
        return
    
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name or f"User_{user_id}"
    message_text = update.message.text
    
    # Check if user is in an active game
    team_info = game_handler.player_teams.get(user_id)
    if not team_info:
        # User not in active game, ignore
        return
    
    logger.info(f"Team chat message from {username} ({user_id}): {message_text[:50]}...")
    
    # Get team members (exclude sender)
    team_players = team_info['team_players']
    team_id = team_info['team_id']
    team_name = get_team_name(team_players)
    
    # Format message with sender info
    formatted_message = f"💬 **{team_name}** - by @{username}\n\n{message_text}"
    
    # Send to all team members except sender
    sent_count = 0
    for player in team_players:
        recipient_id = player.get('user_id')
        if recipient_id != user_id:
            try:
                await context.bot.send_message(
                    chat_id=recipient_id,
                    text=formatted_message,
                    parse_mode='Markdown'
                )
                sent_count += 1
            except Exception as e:
                logger.error(f"Failed to send team chat to user {recipient_id}: {e}")
    
    logger.debug(f"Team chat forwarded to {sent_count} team members")


# ==================== Error Handler ====================

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors with graceful handling of common issues"""
    from telegram.error import Forbidden, BadRequest, TimedOut, NetworkError
    
    error = context.error
    
    # Handle Forbidden errors (bot kicked from group, blocked by user)
    if isinstance(error, Forbidden):
        chat_id = update.effective_chat.id if update.effective_chat else "unknown"
        logger.warning(
            f"Forbidden error in chat {chat_id}: {error}. "
            "Bot may have been kicked or blocked. Silently ignoring."
        )
        return
    
    # Handle BadRequest errors (invalid parameters, etc.)
    if isinstance(error, BadRequest):
        logger.warning(f"BadRequest error: {error}", exc_info=False)
        return
    
    # Handle timeout errors
    if isinstance(error, TimedOut):
        logger.warning(f"Request timed out: {error}", exc_info=False)
        return
    
    # Handle network errors
    if isinstance(error, NetworkError):
        logger.warning(f"Network error: {error}", exc_info=False)
        return
    
    # Log other errors as actual errors
    logger.error(
        f"Unhandled error in update {update.update_id if update else 'unknown'}: {error}",
        exc_info=error,
        extra={
            'update_id': update.update_id if update else None,
            'user_id': update.effective_user.id if update and update.effective_user else None,
            'chat_id': update.effective_chat.id if update and update.effective_chat else None,
            'error_type': type(error).__name__
        }
    )


# ==================== Main ====================

async def post_init(app: Application) -> None:
    """Initialize database connection pool and tables after application is ready"""
    await db_manager.create_pool()
    logger.info("Database connection pool created")
    await db_manager.init_database()
    logger.info("Database initialized")
    
    # Initialize state management tables
    from utils.state_manager import state_manager
    await state_manager.init_state_tables()
    logger.info("State management initialized")


def main():
    """Main bot function with webhook/polling support"""
    logger.info("=" * 50)
    logger.info("Bot starting up...")
    logger.info(f"Mode: {'WEBHOOK' if config.USE_WEBHOOK else 'POLLING'}")
    logger.info("=" * 50)
    
    # Create application
    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).post_init(post_init).build()
    
    # Command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("newgame", newgame_command))
    app.add_handler(CommandHandler("cancelgame", cancelgame_command))
    
    # Character addition conversation
    char_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("addcharacter", addcharacter_start)],
        states={
            CHAR_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, char_name_received)],
            CHAR_MBTI: [CallbackQueryHandler(char_mbti_received, pattern="^mbti_")],
            CHAR_ZODIAC: [CallbackQueryHandler(char_zodiac_received, pattern="^zodiac_")],
            CHAR_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, char_password_received)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)]
    )
    app.add_handler(char_conv_handler)
    
    # Callback handlers
    app.add_handler(CallbackQueryHandler(lobby_callback_handler, pattern="^(join|quit)_lobby$"))
    app.add_handler(CallbackQueryHandler(vote_callback_handler, pattern="^vote_"))
    app.add_handler(CallbackQueryHandler(details_callback_handler, pattern="^details_"))
    app.add_handler(CallbackQueryHandler(back_callback_handler, pattern="^back_"))
    app.add_handler(CallbackQueryHandler(help_callback_handler, pattern="^(show_help|help_.*)$"))
    app.add_handler(CallbackQueryHandler(start_newgame_callback_handler, pattern="^start_newgame$"))
    
    # Team chat handler (should be last to not interfere with commands)
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE & ~filters.COMMAND, team_chat_handler))
    
    # Error handler
    app.add_error_handler(error_handler)
    
    # Start bot in appropriate mode
    if config.USE_WEBHOOK:
        # Webhook mode (Production)
        logger.info(f"Starting webhook server on port {config.PORT}")
        logger.info(f"Webhook URL: {config.WEBHOOK_URL}{config.WEBHOOK_PATH}")
        logger.info("=" * 50)
        
        # Create custom webserver with health check endpoint
        from tornado.web import Application as TornadoApplication, RequestHandler
        
        class HealthCheckHandler(RequestHandler):
            def get(self):
                self.set_header('Content-Type', 'application/json')
                self.write({'status': 'ok', 'bot': 'running'})
        
        # Create Tornado application with health check endpoint
        tornado_app = TornadoApplication([
            (r'/', HealthCheckHandler),
            (r'/health', HealthCheckHandler),
        ])
        
        app.run_webhook(
            listen="0.0.0.0",
            port=config.PORT,
            url_path=config.WEBHOOK_PATH,
            webhook_url=f"{config.WEBHOOK_URL}{config.WEBHOOK_PATH}",
            allowed_updates=Update.ALL_TYPES,
            webhook_server=tornado_app
        )
    else:
        # Polling mode (Local/Development)
        logger.info("Bot is ready and starting to poll for updates...")
        logger.info("=" * 50)
        app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

