"""
Configuration file for Telegram Strategy Game
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Gemini AI Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Game Configuration
LOBBY_SIZE = int(os.getenv('LOBBY_SIZE', 9))
TEAM_SIZE = int(os.getenv('TEAM_SIZE', 3))
ROUND_TIME = int(os.getenv('ROUND_TIME', 60))
NUM_TEAMS = LOBBY_SIZE // TEAM_SIZE  # 3 teams
NUM_ROUNDS = 5
CHARACTERS_PER_VOTING = 4

# Demo/Testing Mode (change LOBBY_SIZE in .env to 1 for solo testing)
DEMO_MODE = LOBBY_SIZE == 1
if DEMO_MODE:
    print("⚠️ DEMO MODE ENABLED - Single player testing")

# Database Configuration (PostgreSQL/Neon)
DATABASE_URL = os.getenv('DATABASE_URL')

# Legacy SQLite path (for migration reference only)
DATABASE_PATH = 'database/game.db'

# Webhook Configuration (Production Mode)
WEBHOOK_URL = os.getenv('WEBHOOK_URL')  # e.g., https://your-app.choreoapis.dev
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH', '/webhook')  # Webhook endpoint path
PORT = int(os.getenv('PORT', 8080))  # Port for webhook server
USE_WEBHOOK = bool(WEBHOOK_URL)  # Auto-detect webhook mode

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_DIR = os.getenv('LOG_DIR', 'logs')
ENABLE_CONSOLE_LOGS = os.getenv('ENABLE_CONSOLE_LOGS', 'true').lower() == 'true'

# Game Status Constants
GAME_STATUS = {
    'LOBBY': 'lobby',
    'IN_PROGRESS': 'in_progress',
    'FINISHED': 'finished'
}

# Validate required configurations
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN must be set in .env file")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY must be set in .env file")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL must be set in .env file")



