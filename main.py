import hashlib
import os
import random
import time
import logging
import cloudscraper
from requests.exceptions import RequestException # Import specifically for the try/except
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Rename this to 'scraper' to avoid conflict with the requests library
scraper = cloudscraper.create_scraper()
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    logging.error("TOKEN not found! Check your environment variables.")

def bump():
    url = "https://discord.com/api/v9/interactions"
    
    # It is safer to set headers per request or via the scraper's session
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
                "description": "Pushes your server to the top of all your server's tags and the front page"
            }
        },
        "nonce": str(random.randint(1, 99999999999999)),
        "analytics_location": "slash_ui"
    }
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Added a 15-second timeout so it doesn't hang indefinitely
            r = scraper.post(url, json=payloads, headers=headers, timeout=15)
            r.raise_for_status()
            logging.info(f"Bump successful! Status: {r.status_code}")
            return True # Exit the function successfully
            
        except Exception as e:
            logging.error(f"Request failed on attempt {attempt + 1}/{max_retries}. Error: {e}")
            
            if "401" in str(e):
                logging.error("Check your TOKEN. Discord says you are Unauthorized.")
                return False # Don't bother retrying if the token is invalid
                
            if attempt < max_retries - 1:
                # Wait 10 to 20 seconds before retrying
                retry_wait = random.randint(10, 20)
                logging.info(f"Retrying in {retry_wait} seconds...")
                time.sleep(retry_wait)
            else:
                logging.error("Max retries reached. Moving on to the main sleep cycle.")
                return False

if __name__ == "__main__":
    while True:
        bump()
        # Sleep for ~2 hours (7200s) + a random buffer
        sleep_time = random.randint(7200, 7800) 
        logging.info(f"Sleeping for {sleep_time // 60} minutes...\n" + "-"*40)
        time.sleep(sleep_time)
