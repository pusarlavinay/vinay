import requests
import os

TOKEN = os.getenv("7349721276:AAE6ZPaQ5gr2pfTzwD4fHdvE3oEayypxtuk")  # Get from environment variables
WEBHOOK_URL = os.getenv("https://vinay-zkni.onrender.com") + "/my_secret_path"  # Append webhook path

response = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}")
print(response.json())
