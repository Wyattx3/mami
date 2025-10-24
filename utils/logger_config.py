"""
Structured Logging Configuration
Professional logging system with rotation and formatting
"""
import logging
import logging.handlers
import os
import sys
from pathlib import Path
from datetime import datetime


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        # Add color to level name
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)


class StructuredLogger:
    """Manages structured logging with file rotation"""
    
    def __init__(self, log_dir: str = "logs", app_name: str = "telegram_bot"):
        self.log_dir = Path(log_dir)
        self.app_name = app_name
        self.log_dir.mkdir(exist_ok=True)
    
    def setup_logging(self, level: str = "INFO", enable_console: bool = True):
        """
        Setup logging configuration
        
        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            enable_console: Whether to enable console logging
        """
        # Convert string level to logging constant
        numeric_level = getattr(logging, level.upper(), logging.INFO)
        
        # Root logger configuration
        root_logger = logging.getLogger()
        root_logger.setLevel(numeric_level)
        
        # Clear existing handlers
        root_logger.handlers.clear()
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        
        colored_formatter = ColoredFormatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # File Handler - All logs
        all_logs_file = self.log_dir / f"{self.app_name}.log"
        file_handler = logging.handlers.RotatingFileHandler(
            all_logs_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(file_handler)
        
        # File Handler - Errors only
        error_logs_file = self.log_dir / f"{self.app_name}_errors.log"
        error_handler = logging.handlers.RotatingFileHandler(
            error_logs_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(error_handler)
        
        # Console Handler
        if enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(numeric_level)
            console_handler.setFormatter(colored_formatter)
            root_logger.addHandler(console_handler)
        
        # Reduce noise from libraries
        logging.getLogger('httpx').setLevel(logging.WARNING)
        logging.getLogger('telegram').setLevel(logging.WARNING)
        logging.getLogger('asyncio').setLevel(logging.WARNING)
        
        logging.info("=" * 70)
        logging.info(f"Logging initialized - Level: {level}")
        logging.info(f"Log directory: {self.log_dir.absolute()}")
        logging.info(f"All logs: {all_logs_file.name}")
        logging.info(f"Error logs: {error_logs_file.name}")
        logging.info("=" * 70)


class LogContext:
    """Context manager for structured logging with additional context"""
    
    def __init__(self, logger: logging.Logger, context: dict):
        self.logger = logger
        self.context = context
        self.old_factory = None
    
    def __enter__(self):
        self.old_factory = logging.getLogRecordFactory()
        
        def record_factory(*args, **kwargs):
            record = self.old_factory(*args, **kwargs)
            for key, value in self.context.items():
                setattr(record, key, value)
            return record
        
        logging.setLogRecordFactory(record_factory)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.setLogRecordFactory(self.old_factory)


class GameLogger:
    """Specialized logger for game events"""
    
    def __init__(self):
        self.logger = logging.getLogger("game")
    
    def log_game_start(self, chat_id: int, player_count: int, lobby_size: int):
        """Log game start event"""
        self.logger.info(
            f"🎮 Game started",
            extra={
                'event_type': 'game_start',
                'chat_id': chat_id,
                'player_count': player_count,
                'lobby_size': lobby_size
            }
        )
    
    def log_game_end(self, chat_id: int, winner_team: str, duration_seconds: int):
        """Log game end event"""
        self.logger.info(
            f"🏆 Game ended - Winner: {winner_team}, Duration: {duration_seconds}s",
            extra={
                'event_type': 'game_end',
                'chat_id': chat_id,
                'winner_team': winner_team,
                'duration_seconds': duration_seconds
            }
        )
    
    def log_round_complete(self, chat_id: int, round_number: int, votes_count: int):
        """Log round completion"""
        self.logger.info(
            f"🎯 Round {round_number} completed with {votes_count} votes",
            extra={
                'event_type': 'round_complete',
                'chat_id': chat_id,
                'round_number': round_number,
                'votes_count': votes_count
            }
        )
    
    def log_player_action(self, user_id: int, chat_id: int, action: str, details: dict = None):
        """Log player action"""
        self.logger.debug(
            f"👤 Player {user_id} - {action}",
            extra={
                'event_type': 'player_action',
                'user_id': user_id,
                'chat_id': chat_id,
                'action': action,
                'details': details or {}
            }
        )
    
    def log_error(self, error_type: str, message: str, details: dict = None):
        """Log game-related error"""
        self.logger.error(
            f"❌ Game Error - {error_type}: {message}",
            extra={
                'event_type': 'game_error',
                'error_type': error_type,
                'details': details or {}
            }
        )


class PerformanceLogger:
    """Logger for performance metrics"""
    
    def __init__(self):
        self.logger = logging.getLogger("performance")
    
    def log_operation_time(self, operation: str, duration_ms: float, success: bool = True):
        """Log operation execution time"""
        status = "✓" if success else "✗"
        level = logging.INFO if success else logging.WARNING
        
        self.logger.log(
            level,
            f"{status} {operation} completed in {duration_ms:.2f}ms",
            extra={
                'operation': operation,
                'duration_ms': duration_ms,
                'success': success
            }
        )
    
    def log_database_query(self, query_type: str, duration_ms: float, rows_affected: int = 0):
        """Log database query performance"""
        self.logger.debug(
            f"💾 DB Query - {query_type}: {duration_ms:.2f}ms, {rows_affected} rows",
            extra={
                'query_type': query_type,
                'duration_ms': duration_ms,
                'rows_affected': rows_affected
            }
        )


# Global instances
structured_logger = StructuredLogger()
game_logger = GameLogger()
performance_logger = PerformanceLogger()


def init_logging(level: str = None, enable_console: bool = True):
    """
    Initialize logging system
    
    Args:
        level: Logging level (defaults to config.LOG_LEVEL or INFO)
        enable_console: Enable console output
    """
    if level is None:
        level = os.getenv('LOG_LEVEL', 'INFO')
    
    structured_logger.setup_logging(level=level, enable_console=enable_console)


# Export utilities
__all__ = [
    'init_logging',
    'LogContext',
    'GameLogger',
    'PerformanceLogger',
    'game_logger',
    'performance_logger'
]

