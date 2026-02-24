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

requests = cloudscraper.create_scraper()
requests.headers = {
    "Authorization": os.getenv("TOKEN"),
}
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
                "description": "Pushes your server to the top of all your server's tags and the front page",
                "description_default": "Pushes your server to the top of all your server's tags and the front page",
                "dm_permission": True,
                "integration_types": [0],
                "global_popularity_rank": 1,
                "options": [],
                "description_localized": "Bumper ce serveur",
                "name_localized": "bump"
            },
            "attachments": []
                "description": "Pushes your server to the top of all your server's tags and the front page"
            }
        },
        "nonce": random.randint(1, 99999999999999),
        "nonce": str(random.randint(1, 99999999999999)),
        "analytics_location": "slash_ui"
    }

    try:
        r = requests.post(url, json=payloads)
        # Using the scraper object here
        r = scraper.post(url, json=payloads, headers=headers)
        r.raise_for_status()
        logging.info(f"Request successful with status code: {r.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        logging.info(f"Bump successful! Status: {r.status_code}")
    except Exception as e:
        logging.error(f"Request failed. Error: {e}")
        if "401" in str(e):
            logging.error("Check your TOKEN. Discord says you are Unauthorized.")

while True:
    bump()
    sleep_time = random.randint(7200, 7800)
    logging.info(f"Sleeping for {sleep_time} seconds")
    time.sleep(sleep_time)
if __name__ == "__main__":
    while True:
        bump()
        # Sleep for ~2 hours (7200s) + a random buffer
        sleep_time = random.randint(7200, 7800) 
        logging.info(f"Sleeping for {sleep_time // 60} minutes...")
        time.sleep(sleep_time)
