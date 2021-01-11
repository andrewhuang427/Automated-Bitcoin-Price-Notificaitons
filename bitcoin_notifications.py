import requests
import time
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()
IFTTT_KEY = os.getenv("IFTTT-KEY")

BITCOIN_PRICE_THRESHOLD = 25000
BITCOIN_API_URL = "https://blockchain.info/ticker"
IFTTT_WEBHOOKS_URL = "https://maker.ifttt.com/trigger/{}/with/key/{}"

def get_latest_bitcoin_price():
    response = requests.get(BITCOIN_API_URL)
    json = response.json()
    bitcoin_price = json["USD"]["last"]
    return float(bitcoin_price)

def post_to_ifttt_webhook(event, value):
    data = {"value1": value}
    url = IFTTT_WEBHOOKS_URL.format(event, IFTTT_KEY)
    requests.post(url, json=data)

def main():
    while True:
        price = get_latest_bitcoin_price()

        # emergency notification
        if price < BITCOIN_PRICE_THRESHOLD:
            post_to_ifttt_webhook("bitcoin_price_emergency", price)

        # normal price update
        else:
            post_to_ifttt_webhook("bitcoin_price_update", price)

        # sleep for 15 minutes
        time.sleep(15 * 60)


if __name__ == "__main__":
    main()
