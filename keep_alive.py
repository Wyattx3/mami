"""
Keep Alive - Simple HTTP server to keep Replit bot running
This prevents the free tier from sleeping after inactivity
"""
from flask import Flask
from threading import Thread
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Telegram Strategy Game Bot</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }
                .container {
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                    padding: 30px;
                    backdrop-filter: blur(10px);
                }
                h1 { text-align: center; }
                .status { 
                    text-align: center; 
                    font-size: 24px;
                    margin: 20px 0;
                }
                .emoji { font-size: 48px; }
                ul { line-height: 2; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎮 Telegram Strategy Game Bot</h1>
                <div class="status">
                    <div class="emoji">✅</div>
                    <strong>Bot is Running!</strong>
                </div>
                <hr>
                <h2>📊 Status</h2>
                <ul>
                    <li>✅ Bot is active and polling</li>
                    <li>✅ Database connected</li>
                    <li>✅ AI service ready</li>
                </ul>
                <h2>🎯 Features</h2>
                <ul>
                    <li>9 players, 3 teams</li>
                    <li>5 rounds of voting</li>
                    <li>AI-powered character matching</li>
                    <li>MBTI & Zodiac personality system</li>
                </ul>
                <hr>
                <p style="text-align: center; margin-top: 30px;">
                    Made with ❤️ in Myanmar 🇲🇲
                </p>
            </div>
        </body>
    </html>
    """

@app.route('/health')
def health():
    return {"status": "healthy", "bot": "running"}, 200

@app.route('/ping')
def ping():
    return "pong", 200

def run():
    """Run Flask server in background thread"""
    try:
        app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)
    except Exception as e:
        logger.error(f"Keep alive server error: {e}")

def keep_alive():
    """Start keep alive server"""
    t = Thread(target=run)
    t.daemon = True
    t.start()
    logger.info("Keep alive server started on port 8080")

