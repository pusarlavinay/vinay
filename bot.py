import os
import telegram
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from telegram.constants import ParseMode
import requests
from flask import Flask, request, jsonify
import threading

# ------------------ Configuration ------------------
TELEGRAM_TOKEN = os.getenv("7349721276:AAG-ZTUlomzo6XQq8iG51smJIttA0qdmy1U)
RENDER_URL = os.getenv("https://vinay-zkni.onrender.com")

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/find_best_code', methods=['POST'])
def find_best_code():
    data = request.get_json()
    query = data.get('query', '')

    # Simulated response (replace with actual API calls)
    best_code = f"Here is a sample response for: {query}"

    return jsonify({'best_code': best_code})

# ------------------ Telegram Bot ------------------
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
            await update.message.reply_text("Sorry, I couldn't find code right now. Please try again later.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def run_telegram():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

# ------------------ Run Flask in Thread ------------------
def run_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_telegram()
