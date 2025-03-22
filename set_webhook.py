import requests
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")  # Get from environment variables
WEBHOOK_URL = os.getenv("RENDER_URL") + "/my_secret_path"  # Append webhook path

response = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}")
print(response.json())
