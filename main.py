import hashlib
import os
import random
import time
import logging
import threading
import cloudscraper
import requests
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Scraper
scraper = cloudscraper.create_scraper()
TOKEN = os.getenv("TOKEN")
APP_URL = os.getenv("APP_URL") # Add your Railway URL to your Environment Variables

if not TOKEN:
    logging.error("TOKEN not found! Check your environment variables.")

# --- RAILWAY KEEP-ALIVE LOGIC ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and bumping!"

def run_web_server():
    # Railway automatically detects the port, but 8080 is a safe default
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def self_ping():
    """Pings the bot's own URL every 10 minutes to prevent Railway from sleeping."""
    if not APP_URL:
        logging.warning("APP_URL variable is missing! Self-ping cannot start.")
        return
        
    time.sleep(30) # Wait for server to boot
    while True:
        try:
            r = requests.get(APP_URL)
            logging.info(f"Self-ping successful (Status: {r.status_code}) - Keeping container awake.")
        except Exception as e:
            logging.error(f"Self-ping failed: {e}")
        time.sleep(600) # Ping every 10 minutes

def start_keep_alive():
    threading.Thread(target=run_web_server, daemon=True).start()
    threading.Thread(target=self_ping, daemon=True).start()
# --------------------------------

def bump():
    url = "https://discord.com/api/v9/interactions"
    headers = {
        "Authorization": TOKEN,
        "Content-Type": "application/json"
    }

    payloads = {
        "type": 2,
        "application_id": "302050872383242240",
        "guild_id": os.getenv("GUILD_ID"),
        "channel_id": os.getenv("CHANNEL_ID"),
        "session_id": hashlib.md5(str(random.randint(1, 99999999999999)).encode()).hexdigest(),
        "data": {
            "version": "1051151064008769576",
            "id": "947088344167366698",
            "name": "bump",
            "type": 1,
            "options": [],
            "application_command": {
                "id": "947088344167366698",
                "type": 1,
                "application_id": "302050872383242240",
                "version": "1051151064008769576",
                "name": "bump",
                "description": "Pushes your server to the top of all your server's tags and the front page",
                "name_localized": "bump"
            }
        },
        "nonce": str(random.randint(1, 99999999999999)),
        "analytics_location": "slash_ui"
    }
    
    try:
        r = scraper.post(url, json=payloads, headers=headers, timeout=20)
        r.raise_for_status()
        logging.info(f"Bump successful! Status: {r.status_code}")
    except Exception as e:
        logging.error(f"Bump failed: {e}")
        if "401" in str(e):
            logging.error("Unauthorized! Check your Discord TOKEN.")

if __name__ == "__main__":
    # Start the keep-alive threads
    logging.info("Initializing Railway Keep-Alive...")
    start_keep_alive()
    
    # Start the main loop
    while True:
        bump()
        # Sleep for ~2 hours + random buffer
        sleep_time = random.randint(7200, 7800) 
        logging.info(f"Sleeping for {sleep_time // 60} minutes...")
        time.sleep(sleep_time)
