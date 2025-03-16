from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Take the bot token from environment variable (DO NOT hardcode in code)
BOT_TOKEN = os.environ.get("7349721276:AAG-ZTUlomzo6XQq8iG51smJIttA0qdmy1U")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Home route to test if bot is live
@app.route('/')
def home():
    return '🤖 Bot is running successfully!'

# Webhook route to receive Telegram updates
@app.route('/telegram_webhook', methods=['POST'])
def telegram_webhook():
    data = request.json
    print("Received data:", data)  # To see incoming message in Render logs

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')
        reply_text = f"You said: {text}"
        send_message(chat_id, reply_text)

    return '', 200  # Reply OK to Telegram

# Function to send message to user
def send_message(chat_id, text):
    payload = {'chat_id': chat_id, 'text': text}
    response = requests.post(TELEGRAM_API_URL, json=payload)
    print("Message sent:", response.json())  # Check in logs

# Run locally for testing (Render uses gunicorn to run)
if __name__ == '__main__':
    app.run(debug=True, port=5000)
