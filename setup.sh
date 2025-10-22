#!/bin/bash

echo "🎮 Telegram Strategy Game - Setup Script"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python is installed"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env file from template..."
    
    cat > .env << EOF
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Gemini AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Game Configuration
LOBBY_SIZE=9
TEAM_SIZE=3
ROUND_TIME=60
EOF
    
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file and add your API keys:"
    echo "   - TELEGRAM_BOT_TOKEN"
    echo "   - GEMINI_API_KEY"
    echo ""
else
    echo "✅ .env file exists"
    echo ""
fi

# Create database directory
echo "Creating database directory..."
mkdir -p database

echo "✅ Database directory created"
echo ""

echo "========================================"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys: nano .env"
echo "2. Add characters to database: python bot.py (then use /addcharacter)"
echo "3. Run the bot: python bot.py"
echo ""
echo "To activate virtual environment in future:"
echo "  source venv/bin/activate"
echo ""
echo "Have fun! 🎉"


