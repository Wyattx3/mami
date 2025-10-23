"""
Improved Game Handler with Better Private Message Handling
This is an upgrade to the existing game_handler.py with:
- Retry logic for failed messages
- Rate limiting
- Better error handling
- Fallback notifications
"""

import asyncio
import logging
from typing import Dict, List, Any
from telegram.error import Forbidden, BadRequest, TimedOut, NetworkError

logger = logging.getLogger(__name__)


class ImprovedPrivateMessageHandler:
    """Handles private message delivery with retries and rate limiting"""
    
    def __init__(self):
        self.rate_limit = 30  # messages per second
        self.delay_between_messages = 1.0 / self.rate_limit  # ~33ms
        self.max_retries = 3
        self.retry_delays = [1.0, 2.0, 4.0]  # exponential backoff
        
    async def send_private_results_improved(self, context, game_id: int, 
                                           teams: Dict[int, List[Dict[str, Any]]],
                                           results: Dict[int, Dict[str, Any]], 
                                           winner: int, chat_id: int):
        """
        Send private results to all players with improved error handling
        
        Features:
        - Rate limiting (30 msg/sec)
        - Retry logic (3 attempts)
        - Error categorization
        - Fallback group notification
        """
        logger.info(f"Game {game_id} - Sending private results to all players")
        
        # Prepare winner info
        from utils.helpers import get_team_name
        winner_team_name = get_team_name(results[winner].get('players', []))
        winner_score = results[winner]['total_score']
        
        # Track delivery status
        delivery_stats = {
            'success': 0,
            'failed': 0,
            'user_not_started': [],
            'user_blocked': [],
            'timeout': [],
            'other': []
        }
        
        # Process each team
        for team_id, team_players in teams.items():
            team_name = get_team_name(team_players)
            team_data = results.get(team_id, {})
            team_score = team_data.get('total_score', 0)
            
            # Build team result message
            lines = [
                f"📊 **Game Results - {team_name}**\n",
                f"🎮 Game ID: {game_id}\n"
            ]
            
            # Show team's rounds
            if 'rounds' in team_data:
                lines.append("**သင့် Team ရဲ့ ရလဒ်များ:**\n")
                for round_data in team_data['rounds']:
                    role = round_data.get('role', 'Unknown')
                    char_name = round_data.get('character_name', 'Optional')
                    score = round_data.get('score', 0)
                    lines.append(f"• **{role}**: {char_name} ({score}/10 မှတ်)")
                
                lines.append(f"\n**Total Score:** {team_score} မှတ်\n")
            
            # Show winner
            if team_id == winner:
                lines.append("🎉 **သင့် Team က အနိုင်ရခဲ့ပါတယ်!** 🎉")
            else:
                lines.append(f"👑 **Winner:** {winner_team_name} ({winner_score} မှတ်)")
            
            private_message = "\n".join(lines)
            
            # Send to all players in team with rate limiting and retries
            for player in team_players:
                user_id = player.get('user_id')
                username = player.get('username', 'Unknown')
                
                # Send with retry logic
                success, error_type = await self._send_with_retry(
                    context, user_id, private_message
                )
                
                if success:
                    delivery_stats['success'] += 1
                    logger.debug(f"Private result sent to {username} ({user_id})")
                else:
                    delivery_stats['failed'] += 1
                    logger.warning(f"Failed to send private result to {username} ({user_id}): {error_type}")
                    
                    # Categorize error
                    if error_type == 'forbidden':
                        delivery_stats['user_not_started'].append(username)
                    elif error_type == 'blocked':
                        delivery_stats['user_blocked'].append(username)
                    elif error_type == 'timeout':
                        delivery_stats['timeout'].append(username)
                    else:
                        delivery_stats['other'].append(username)
                
                # Rate limiting
                await asyncio.sleep(self.delay_between_messages)
        
        # Log delivery statistics
        logger.info(f"Game {game_id} - Private message delivery: "
                   f"Success: {delivery_stats['success']}, "
                   f"Failed: {delivery_stats['failed']}")
        
        # Send fallback notification if there were failures
        if delivery_stats['failed'] > 0:
            await self._send_fallback_notification(
                context, chat_id, game_id, delivery_stats
            )
        
        return delivery_stats
    
    async def _send_with_retry(self, context, user_id: int, message: str) -> tuple:
        """
        Send message with retry logic
        
        Returns:
            (success: bool, error_type: str)
        """
        for attempt in range(self.max_retries):
            try:
                await context.bot.send_message(
                    chat_id=user_id,
                    text=message,
                    parse_mode='Markdown'
                )
                return (True, None)
                
            except Forbidden as e:
                # User hasn't started bot or blocked it
                error_msg = str(e).lower()
                if 'bot was blocked' in error_msg:
                    return (False, 'blocked')
                else:
                    return (False, 'forbidden')
            
            except BadRequest as e:
                # Invalid request (shouldn't happen with valid user_id)
                logger.error(f"BadRequest for user {user_id}: {e}")
                return (False, 'bad_request')
            
            except TimedOut:
                # Timeout - retry
                if attempt < self.max_retries - 1:
                    logger.warning(f"Timeout for user {user_id}, retrying...")
                    await asyncio.sleep(self.retry_delays[attempt])
                else:
                    return (False, 'timeout')
            
            except NetworkError as e:
                # Network error - retry
                if attempt < self.max_retries - 1:
                    logger.warning(f"Network error for user {user_id}: {e}, retrying...")
                    await asyncio.sleep(self.retry_delays[attempt])
                else:
                    return (False, 'network')
            
            except Exception as e:
                # Unknown error
                logger.error(f"Unexpected error sending to user {user_id}: {e}")
                return (False, 'other')
        
        return (False, 'max_retries')
    
    async def _send_fallback_notification(self, context, chat_id: int, 
                                         game_id: int, stats: dict):
        """Send fallback notification to group chat for failed deliveries"""
        
        failed_count = stats['failed']
        success_count = stats['success']
        
        notification_lines = [
            f"📊 **Game {game_id} - Results Delivery Report**\n",
            f"✅ Successfully sent: {success_count} players",
            f"❌ Failed to send: {failed_count} players\n"
        ]
        
        # Detail failures
        if stats['user_not_started']:
            notification_lines.append(
                f"⚠️  **{len(stats['user_not_started'])} players** haven't started the bot:"
            )
            for username in stats['user_not_started'][:5]:  # Show first 5
                notification_lines.append(f"   • @{username}")
            if len(stats['user_not_started']) > 5:
                notification_lines.append(f"   • ... နှင့် {len(stats['user_not_started']) - 5} ဦး")
            notification_lines.append("")
        
        if stats['user_blocked']:
            notification_lines.append(
                f"🚫 **{len(stats['user_blocked'])} players** have blocked the bot"
            )
            notification_lines.append("")
        
        if stats['timeout'] or stats['other']:
            total_errors = len(stats['timeout']) + len(stats['other'])
            notification_lines.append(
                f"⚠️  **{total_errors} players** had technical issues (timeout/network)"
            )
            notification_lines.append("")
        
        # Add help message
        if stats['user_not_started']:
            notification_lines.append(
                "💡 **Action Required:**\n"
                "ကျေးဇူးပြု၍ bot ကို private chat မှာ /start နှိပ်ပြီး "
                "နောက်ထပ် game များတွင် results များ လက်ခံရယူပါ။"
            )
        
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text="\n".join(notification_lines),
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Failed to send fallback notification: {e}")


# Global instance
improved_message_handler = ImprovedPrivateMessageHandler()

