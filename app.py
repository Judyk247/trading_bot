import threading
import os
from flask import Flask
from trading_bot import setup_bot

# Create Flask web app
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is alive!", 200

@app.route('/health')
def health():
    return "OK", 200

# Function to start the Telegram bot in a background thread
def start_telegram_bot():
    bot_app = setup_bot()
    print("Starting Telegram bot polling...")
    bot_app.run_polling()

# When this script is run, start both the web server and the bot
if __name__ == "__main__":
    # Start bot in a separate thread so web server can run concurrently
    bot_thread = threading.Thread(target=start_telegram_bot)
    bot_thread.daemon = True
    bot_thread.start()

    # Get port from environment (Render sets PORT automatically)
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting web server on port {port}")
    app.run(host="0.0.0.0", port=port)
