from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
BOT_TOKEN = TELEGRAM_BOT_TOKEN  # Use token from env var
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.route('/')
def home():
    return '🤖 Bot is running successfully!'

# Webhook route
@app.route('/telegram_webhook', methods=['POST'])
def telegram_webhook():
    data = request.json
    print("Received data:", data)

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')
        reply_text = f"You said: {text}"
        send_message(chat_id, reply_text)
    return '', 200

def send_message(chat_id, text):
    payload = {'chat_id': chat_id, 'text': text}
    response = requests.post(TELEGRAM_API_URL, json=payload)
    print("Message sent:", response.json())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
