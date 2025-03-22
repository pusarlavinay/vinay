import requests

TOKEN = "7349721276:AAG-ZTUlomzo6XQq8iG51smJIttA0qdmy1U"  # Replace this with your real bot token

WEBHOOK_URL = "https://geniecode.onrender.com/my_secret_path"  # Your Render URL + webhook path

response = requests.get(
    f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}"
)

print(response.json())
