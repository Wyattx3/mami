"""
Comprehensive Error Handling System
Defensive programming with detailed logging
"""
import logging
import traceback
from typing import Optional, Callable, Any
from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


class BotError(Exception):
    """Base exception for bot errors"""
    def __init__(self, message: str, user_message: Optional[str] = None):
        self.message = message
        self.user_message = user_message or "စက်ပိုင်းဆိုင်ရာ အမှားတစ်ခု ဖြစ်ပေါ်ခဲ့ပါသည်။ ထပ်မံကြိုးစားကြည့်ပါ။"
        super().__init__(self.message)


class ValidationError(BotError):
    """Raised when user input validation fails"""
    pass


class DatabaseError(BotError):
    """Raised when database operations fail"""
    pass


class GameError(BotError):
    """Raised when game logic errors occur"""
    pass


def safe_execute(error_message: str = "Operation failed", 
                return_value: Any = None,
                log_level: str = "error"):
    """
    Decorator for safe function execution with error handling
    
    Args:
        error_message: Message to log on error
        return_value: Value to return on error
        log_level: Logging level (error, warning, critical)
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except BotError as e:
                # Known bot errors
                logger.log(
                    getattr(logging, log_level.upper()),
                    f"{error_message}: {e.message}",
                    exc_info=False
                )
                return return_value
            except Exception as e:
                # Unknown errors
                logger.critical(
                    f"{error_message} - Unexpected error: {str(e)}",
                    exc_info=True
                )
                return return_value
        return wrapper
    return decorator


class InputValidator:
    """Validates user input with comprehensive error messages"""
    
    @staticmethod
    def validate_number(text: str, min_val: Optional[int] = None, 
                       max_val: Optional[int] = None) -> tuple[bool, Optional[int], str]:
        """
        Validate if text is a valid number within range
        
        Returns:
            (is_valid, value, error_message)
        """
        try:
            value = int(text)
            
            if min_val is not None and value < min_val:
                return False, None, f"❌ နံပါတ်သည် {min_val} ထက် မနည်းရပါ။"
            
            if max_val is not None and value > max_val:
                return False, None, f"❌ နံပါတ်သည် {max_val} ထက် မကျော်ရပါ။"
            
            return True, value, ""
            
        except ValueError:
            return False, None, "❌ ကျေးဇူးပြု၍ ကိန်းဂဏန်း (Number) သာ ရိုက်ထည့်ပါ။"
    
    @staticmethod
    def validate_username(username: str) -> tuple[bool, str]:
        """
        Validate username
        
        Returns:
            (is_valid, error_message)
        """
        if not username or len(username.strip()) == 0:
            return False, "❌ အမည်ကို ဖြည့်သွင်းပါ။"
        
        if len(username) < 2:
            return False, "❌ အမည်သည် အနည်းဆုံး ၂ လုံး ရှိရပါမည်။"
        
        if len(username) > 50:
            return False, "❌ အမည်သည် ၅၀ လုံးထက် မကျော်ရပါ။"
        
        return True, ""
    
    @staticmethod
    def validate_chat_type(update: Update, allowed_types: list[str]) -> tuple[bool, str]:
        """
        Validate if command is used in correct chat type
        
        Args:
            update: Telegram update
            allowed_types: List of allowed chat types ('private', 'group', 'supergroup')
        
        Returns:
            (is_valid, error_message)
        """
        chat_type = update.effective_chat.type
        
        if chat_type not in allowed_types:
            if 'private' in allowed_types:
                return False, "❌ ဒီ command ကို private chat မှာသာ သုံးနိုင်ပါတယ်။"
            else:
                return False, "❌ ဒီ command ကို group chat မှာသာ သုံးနိုင်ပါတယ်။"
        
        return True, ""


class ErrorReporter:
    """Reports errors to users with friendly messages"""
    
    @staticmethod
    async def report_error(update: Update, context: ContextTypes.DEFAULT_TYPE, 
                          error: Exception, user_message: Optional[str] = None):
        """
        Report error to user with friendly message
        
        Args:
            update: Telegram update
            context: Bot context
            error: Exception that occurred
            user_message: Custom message for user (optional)
        """
        try:
            # Log the error
            logger.error(
                f"Error in update {update.update_id}: {str(error)}",
                exc_info=True,
                extra={
                    'user_id': update.effective_user.id if update.effective_user else None,
                    'chat_id': update.effective_chat.id if update.effective_chat else None,
                    'update_type': update.effective_message.text if update.effective_message else 'unknown'
                }
            )
            
            # Determine user-friendly message
            if isinstance(error, ValidationError):
                message = error.user_message
            elif isinstance(error, DatabaseError):
                message = "💾 Database ချိတ်ဆက်မှု ပြဿနာ ဖြစ်ပေါ်နေပါသည်။ ခဏစောင့်ပြီး ထပ်မံကြိုးစားပါ။"
            elif isinstance(error, GameError):
                message = error.user_message
            elif user_message:
                message = user_message
            else:
                message = "⚠️ တစ်စုံတစ်ခု မှားယွင်းသွားပါသည်။ ထပ်မံကြိုးစားကြည့်ပါ။"
            
            # Send message to user
            if update.effective_message:
                await update.effective_message.reply_text(message)
            elif update.callback_query:
                await update.callback_query.answer(message, show_alert=True)
                
        except Exception as e:
            # Error while reporting error - just log it
            logger.critical(f"Failed to report error to user: {e}", exc_info=True)
    
    @staticmethod
    async def report_validation_error(update: Update, context: ContextTypes.DEFAULT_TYPE, 
                                     error_message: str):
        """Quick helper to report validation errors"""
        try:
            if update.effective_message:
                await update.effective_message.reply_text(f"⚠️ {error_message}")
            elif update.callback_query:
                await update.callback_query.answer(error_message, show_alert=True)
        except Exception as e:
            logger.error(f"Failed to send validation error: {e}")


class SafeOperations:
    """Safe wrappers for common operations"""
    
    @staticmethod
    @safe_execute("Failed to send message", return_value=False)
    async def safe_send_message(context: ContextTypes.DEFAULT_TYPE, 
                               chat_id: int, text: str, **kwargs) -> bool:
        """Safely send message with error handling"""
        await context.bot.send_message(chat_id=chat_id, text=text, **kwargs)
        return True
    
    @staticmethod
    @safe_execute("Failed to edit message", return_value=False)
    async def safe_edit_message(query, text: str, **kwargs) -> bool:
        """Safely edit message with error handling"""
        await query.edit_message_text(text=text, **kwargs)
        return True
    
    @staticmethod
    @safe_execute("Failed to answer callback", return_value=False)
    async def safe_answer_callback(query, text: str = None, **kwargs) -> bool:
        """Safely answer callback query with error handling"""
        await query.answer(text=text, **kwargs)
        return True


def handle_command_errors(func: Callable):
    """Decorator for command handlers with comprehensive error handling"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            return await func(update, context)
        except ValidationError as e:
            await ErrorReporter.report_validation_error(update, context, e.user_message)
        except BotError as e:
            await ErrorReporter.report_error(update, context, e)
        except Exception as e:
            logger.critical(
                f"Unhandled error in {func.__name__}: {str(e)}",
                exc_info=True,
                extra={
                    'function': func.__name__,
                    'user_id': update.effective_user.id if update.effective_user else None,
                    'chat_id': update.effective_chat.id if update.effective_chat else None
                }
            )
            await ErrorReporter.report_error(update, context, e)
    return wrapper


def handle_callback_errors(func: Callable):
    """Decorator for callback handlers with comprehensive error handling"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        try:
            await query.answer()  # Always acknowledge callback
            return await func(update, context)
        except ValidationError as e:
            await query.answer(e.user_message, show_alert=True)
        except BotError as e:
            await query.answer(e.user_message, show_alert=True)
            logger.error(f"Bot error in {func.__name__}: {e.message}", exc_info=True)
        except Exception as e:
            logger.critical(
                f"Unhandled error in {func.__name__}: {str(e)}",
                exc_info=True,
                extra={
                    'function': func.__name__,
                    'user_id': update.effective_user.id if update.effective_user else None,
                    'chat_id': update.effective_chat.id if update.effective_chat else None,
                    'callback_data': query.data
                }
            )
            await query.answer(
                "⚠️ တစ်စုံတစ်ခု မှားယွင်းသွားပါသည်။",
                show_alert=True
            )
    return wrapper


# Export commonly used utilities
__all__ = [
    'BotError',
    'ValidationError',
    'DatabaseError',
    'GameError',
    'InputValidator',
    'ErrorReporter',
    'SafeOperations',
    'handle_command_errors',
    'handle_callback_errors',
    'safe_execute'
]

