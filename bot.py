import os
import logging
import telegram
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from flask import Flask, request, jsonify

# ------------------ Configuration ------------------
TELEGRAM_TOKEN = os.getenv("7349721276:AAE6ZPaQ5gr2pfTzwD4fHdvE3oEayypxtuk")  # Get token from environment variable
WEBHOOK_URL = os.getenv("https://vinay-zkni.onrender.com")  # Your Render webhook URL

# Initialize Telegram Bot
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# ------------------ Flask Backend ------------------
app = Flask(__name__)

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@app.route("/")
def home():
    return "Bot is running!"

@app.route('/telegram_webhook', methods=['POST'])
def telegram_webhook():
    """Handles incoming Telegram updates."""
    data = request.get_json()
    logging.info(f"Received update from Telegram: {data}")

    if "message" in data:
        update = telegram.Update.de_json(data, application.bot)
        application.process_update(update)
        logging.info("Update processed successfully!")

    return jsonify({"status": "ok"}), 200  # Send a valid response to Telegram

# ------------------ Telegram Bot Commands ------------------
async def start(update, context):
    await update.message.reply_text("Hello! I am your bot. Send me a message!")

async def handle_message(update, context):
    user_text = update.message.text
    await update.message.reply_text(f"You said: {user_text}")

# ------------------ Register Handlers ------------------
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# ------------------ Start Flask Server ------------------
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))  # Use PORT assigned by Render
    app.run(host="0.0.0.0", port=PORT)
