import os
import telegram
import logging
import requests
from flask import Flask, request, jsonify
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from telegram.constants import ParseMode

# ------------------ Configuration ------------------
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "7349721276:AAG-ZTUlomzo6XQq8iG51smJIttA0qdmy1U")
RENDER_URL = os.getenv("RENDER_URL", "https://vinay-zkni.onrender.com")

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ------------------ Telegram Bot ------------------
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

async def start(update, context):
    await update.message.reply_text("Hello! Send me a coding problem, and I'll find the best code snippet!")

async def handle_message(update, context):
    query = update.message.text
    await update.message.reply_text("Looking for the best code snippet...⏳")

    try:
        response = requests.post(f"{RENDER_URL}/find_best_code", json={'query': query})
        if response.status_code == 200:
            best_code = response.json().get('best_code', 'No code found.')
            await update.message.reply_text(f"Here is the best code I found:\n\n<pre>{best_code}</pre>", parse_mode=ParseMode.HTML)
        else:
            await update.message.reply_text("Error fetching the code snippet.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# ------------------ Webhook Route ------------------
@app.route('/telegram_webhook', methods=['POST'])
def telegram_webhook():
    """Handles incoming Telegram updates."""
    data = request.get_json()
    logging.info(f"Received update from Telegram: {data}")

    if "message" in data:
        update = telegram.Update.de_json(data, application.bot)
        application.process_update(update)
    
    return jsonify({"status": "ok"}), 200

# ------------------ Flask API Endpoints ------------------
@app.route('/')
def home():
    return "Bot is running!"

@app.route('/find_best_code', methods=['POST'])
def find_best_code():
    data = request.get_json()
    query = data.get('query', '')

    best_code = f"Here is a sample response for: {query}"
    return jsonify({'best_code': best_code})

# ------------------ Run Flask in Thread ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
