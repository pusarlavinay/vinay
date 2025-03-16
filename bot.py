import os
import telegram
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
from telegram.constants import ParseMode
import requests
from bs4 import BeautifulSoup
import logging
from flask import Flask, request, jsonify
import threading
import base64
import google.generativeai as genai

# ------------------ Configuration ------------------
# Replace these with your own tokens/keys
TELEGRAM_TOKEN = "7349721276:AAG-ZTUlomzo6XQq8iG51smJIttA0qdmy1U"
GEMINI_API_KEY = "AIzaSyBbUyXOogNmFNZxTpxQ-1nz289Xnk2tLCU"
DEEPSEEK_API_KEY = "sk-9315c0a8d43846b69e4158a8e08e5f3b"
GITHUB_TOKEN = "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"
RENDER_URL = "https://vinay-zkni.onrender.com"  # Your Render backend URL
DEEPSEEK_API_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"  # DeepSeek endpoint

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ------------------ Flask Backend ------------------
app = Flask(__name__)

@app.route('/find_best_code', methods=['POST'])
def find_best_code():
    data = request.get_json()
    query = data['query']
    logging.info(f"Received query in Flask: {query}")

    # Get responses
    gemini_code = get_gemini_code(query)
    deepseek_code = get_deepseek_code(query)
    web_snippets = scrape_code_from_websites(query)
    github_snippets = scrape_code_from_github(query)

    all_snippets = [gemini_code, deepseek_code] + web_snippets + github_snippets
    best_code = compare_codes(all_snippets, query)

    return jsonify({'best_code': best_code})

# ------------------ Gemini API ------------------
def get_gemini_code(query):
    try:
        response = gemini_model.generate_content(query)
        return response.text
    except Exception as e:
        logging.error(f"Gemini error: {e}")
        return f"Gemini error: {e}"

# ------------------ DeepSeek API ------------------
def get_deepseek_code(query):
    try:
        headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "deepseek-coder-33b-instruct",
            "messages": [{"role": "user", "content": query}],
            "temperature": 0.7
        }
        response = requests.post(DEEPSEEK_API_ENDPOINT, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"DeepSeek API error: {response.status_code}"
    except Exception as e:
        logging.error(f"DeepSeek error: {e}")
        return f"DeepSeek error: {e}"

# ------------------ Web Scraping ------------------
def scrape_code_from_websites(query):
    snippets = []
    try:
        search_url = f"https://www.google.com/search?q={query}+code"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        links = [a['href'] for a in soup.select('a[href^="http"]')]
        for link in links:
            code = scrape_code_from_url(link)
            if code:
                snippets.append(code)
    except Exception as e:
        logging.error(f"Web scraping error: {e}")
    return snippets

# ------------------ GitHub Scraping ------------------
def scrape_code_from_github(query):
    snippets = []
    try:
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        url = f"https://api.github.com/search/code?q={query}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            items = response.json().get("items", [])
            for item in items:
                download_url = item.get("git_url")
                if download_url:
                    code_response = requests.get(download_url, headers=headers)
                    if code_response.status_code == 200:
                        snippets.append(code_response.text)
    except Exception as e:
        logging.error(f"GitHub error: {e}")
    return snippets

def scrape_code_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        code_blocks = soup.find_all("code")
        return code_blocks[0].text if code_blocks else None
    except Exception as e:
        logging.error(f"URL scraping error: {e}")
        return None

# ------------------ Code Comparison ------------------
def compare_codes(snippets, query):
    if not snippets:
        return "No code found."
    best_code = snippets[0]
    best_score = 0
    for code in snippets:
        score = calculate_code_score(code, query)
        if score > best_score:
            best_code, best_score = code, score
    return best_code

def calculate_code_score(code, query):
    score = 1 if query.lower() in code.lower() else 0
    score += len(code) * -0.001  # Penalize long code
    return score

# ------------------ Telegram Bot ------------------
async def start(update, context):
    await update.message.reply_text("Hello! Send me a coding problem, and I'll find the best code snippet!")

async def handle_message(update, context):
    query = update.message.text
    await update.message.reply_text("Looking for the best code snippet...⏳")

    try:
        response = requests.post(RENDER_URL, json={'query': query})
        if response.status_code == 200:
            best_code = response.json().get('best_code', 'No code found.')
            await update.message.reply_text(f"Here is the best code I found:\n\n<pre>{best_code}</pre>", parse_mode=ParseMode.HTML)
        else:
            await update.message.reply_text("Sorry, I couldn't find code right now. Please try again later.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# ------------------ Run Flask in Thread ------------------
def run_flask():
    app.run(host='0.0.0.0', port=10000)

# ------------------ Run Telegram Bot ------------------
def run_telegram():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

# ------------------ Main ------------------
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_telegram()
