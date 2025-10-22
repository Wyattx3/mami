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

# Database Configuration
DATABASE_PATH = 'database/game.db'

# Validate required configurations
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN must be set in .env file")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY must be set in .env file")



