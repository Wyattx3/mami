"""
Keep alive server for Replit free tier
Prevents the bot from sleeping by responding to HTTP requests
"""
from flask import Flask
from threading import Thread
import logging

app = Flask('')

@app.route('/')
def home():
    return "Bot is running! 🤖"

@app.route('/health')
def health():
    return {"status": "healthy", "bot": "Telegram Strategy Game"}

def run():
    """Run Flask server in background"""
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    """Start keep alive server"""
    logging.info("Starting keep alive server...")
    t = Thread(target=run)
    t.daemon = True
    t.start()
    logging.info("Keep alive server started on port 8080")
