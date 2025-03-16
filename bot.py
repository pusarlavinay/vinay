from flask import Flask, request
import requests

app = Flask(__name__)

# Replace this with your bot's token
BOT_TOKEN = '7349721276:AAG-ZTUlomzo6XQq8iG51smJIttA0qdmy1U'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'


@app.route('/')
def home():
    return "Telegram Bot is running!"


@app.route('/telegram_webhook', methods=['POST'])
def telegram_webhook():
    if request.method == 'POST':
        data = request.json
        print(f"Received data: {data}")  # Log incoming updates

        # Extract chat ID and message
        chat_id = data['message']['chat']['id']
        user_message = data['message'].get('text', '')

        # Formulate a response
        reply = f"You said: {user_message}"

        # Send response back to Telegram
        send_message(chat_id, reply)

        return {'status': 'ok'}
    return {'status': 'not ok'}


def send_message(chat_id, text):
    """Send message to Telegram chat."""
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(TELEGRAM_API_URL, json=payload)
    print(f"Message sent response: {response.json()}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
