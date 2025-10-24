"""
Reliable Message Delivery System
Prevents data loss with retry logic and delivery tracking
"""
import asyncio
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError, TimedOut, NetworkError, RetryAfter

logger = logging.getLogger(__name__)


class MessageDelivery:
    """Handle reliable message delivery with retry logic"""
    
    def __init__(self):
        self.max_retries = 3
        self.retry_delays = [2, 5, 10]  # Exponential backoff (increased for better reliability)
        self.failed_messages: List[Dict[str, Any]] = []
    
    async def send_message_with_retry(
        self,
        bot: Bot,
        chat_id: int,
        text: str,
        **kwargs
    ) -> Optional[Any]:
        """Send message with retry logic
        
        Args:
            bot: Telegram Bot instance
            chat_id: Target chat ID
            text: Message text
            **kwargs: Additional parameters for send_message
            
        Returns:
            Message object if successful, None if all retries failed
        """
        for attempt in range(self.max_retries):
            try:
                message = await bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    **kwargs
                )
                
                if attempt > 0:
                    logger.info(f"Message delivered to {chat_id} after {attempt + 1} attempts")
                
                return message
                
            except RetryAfter as e:
                # Rate limited - wait as told by Telegram
                wait_time = e.retry_after + 1
                logger.warning(f"Rate limited. Waiting {wait_time}s before retry")
                await asyncio.sleep(wait_time)
                
            except TimedOut as e:
                # Network timeout
                if attempt < self.max_retries - 1:
                    wait_time = self.retry_delays[attempt]
                    logger.warning(
                        f"Timeout sending to {chat_id}. "
                        f"Retry {attempt + 1}/{self.max_retries} in {wait_time}s"
                    )
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"All retries exhausted for {chat_id} (Timeout)")
                    self._store_failed_message(chat_id, text, "Timeout", kwargs)
                    
            except NetworkError as e:
                # Network error
                if attempt < self.max_retries - 1:
                    wait_time = self.retry_delays[attempt]
                    logger.warning(
                        f"Network error sending to {chat_id}. "
                        f"Retry {attempt + 1}/{self.max_retries} in {wait_time}s"
                    )
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"All retries exhausted for {chat_id} (NetworkError)")
                    self._store_failed_message(chat_id, text, "NetworkError", kwargs)
                    
            except TelegramError as e:
                # Other Telegram errors (Forbidden, BadRequest, etc.)
                error_msg = str(e)
                
                if "blocked" in error_msg.lower() or "forbidden" in error_msg.lower():
                    # User blocked the bot - no point retrying
                    logger.warning(f"User {chat_id} blocked the bot: {e}")
                    return None
                    
                if attempt < self.max_retries - 1:
                    wait_time = self.retry_delays[attempt]
                    logger.warning(
                        f"Telegram error sending to {chat_id}: {e}. "
                        f"Retry {attempt + 1}/{self.max_retries} in {wait_time}s"
                    )
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"All retries exhausted for {chat_id}: {e}")
                    self._store_failed_message(chat_id, text, str(e), kwargs)
                    
            except Exception as e:
                # Unexpected error
                logger.error(f"Unexpected error sending to {chat_id}: {e}", exc_info=True)
                self._store_failed_message(chat_id, text, f"Unexpected: {e}", kwargs)
                break
        
        return None
    
    async def send_bulk_messages(
        self,
        bot: Bot,
        recipients: List[Dict[str, Any]],
        text_template: str,
        rate_limit_delay: float = 0.05,
        **common_kwargs
    ) -> Dict[str, int]:
        """Send messages to multiple recipients with rate limiting
        
        Args:
            bot: Telegram Bot instance
            recipients: List of recipient dicts with 'chat_id' and optional 'text' or template data
            text_template: Message template
            rate_limit_delay: Delay between messages (seconds)
            **common_kwargs: Common parameters for all messages
            
        Returns:
            Dict with 'sent', 'failed' counts
        """
        sent_count = 0
        failed_count = 0
        
        for i, recipient in enumerate(recipients):
            chat_id = recipient.get('chat_id')
            if not chat_id:
                continue
            
            # Format message
            text = recipient.get('text', text_template)
            if '{' in text:
                # Template variables
                text = text.format(**recipient)
            
            # Send with retry
            result = await self.send_message_with_retry(
                bot, chat_id, text, **common_kwargs
            )
            
            if result:
                sent_count += 1
            else:
                failed_count += 1
            
            # Rate limiting (except for last message)
            if i < len(recipients) - 1:
                await asyncio.sleep(rate_limit_delay)
        
        logger.info(
            f"Bulk send complete: {sent_count} sent, {failed_count} failed "
            f"out of {len(recipients)} total"
        )
        
        return {'sent': sent_count, 'failed': failed_count}
    
    def _store_failed_message(
        self,
        chat_id: int,
        text: str,
        error: str,
        kwargs: Dict[str, Any]
    ):
        """Store failed message for later retry or logging"""
        failed_msg = {
            'chat_id': chat_id,
            'text': text,
            'error': error,
            'kwargs': kwargs,
            'timestamp': datetime.now(),
            'retry_count': self.max_retries
        }
        
        self.failed_messages.append(failed_msg)
        logger.error(
            f"Failed message stored: chat_id={chat_id}, "
            f"error={error}, retry_count={self.max_retries}"
        )
    
    def get_failed_messages(self) -> List[Dict[str, Any]]:
        """Get all failed messages"""
        return self.failed_messages.copy()
    
    def clear_failed_messages(self):
        """Clear failed messages list"""
        count = len(self.failed_messages)
        self.failed_messages.clear()
        logger.info(f"Cleared {count} failed messages")
    
    async def retry_failed_messages(self, bot: Bot) -> Dict[str, int]:
        """Retry all failed messages
        
        Returns:
            Dict with 'sent', 'failed' counts
        """
        if not self.failed_messages:
            logger.info("No failed messages to retry")
            return {'sent': 0, 'failed': 0}
        
        logger.info(f"Retrying {len(self.failed_messages)} failed messages...")
        
        sent_count = 0
        still_failed = []
        
        for msg in self.failed_messages:
            result = await self.send_message_with_retry(
                bot,
                msg['chat_id'],
                msg['text'],
                **msg['kwargs']
            )
            
            if result:
                sent_count += 1
            else:
                still_failed.append(msg)
        
        # Update failed messages list
        self.failed_messages = still_failed
        
        logger.info(
            f"Retry complete: {sent_count} sent, {len(still_failed)} still failed"
        )
        
        return {'sent': sent_count, 'failed': len(still_failed)}


# Global message delivery instance
message_delivery = MessageDelivery()

