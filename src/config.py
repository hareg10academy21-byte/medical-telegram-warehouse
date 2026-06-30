from dotenv import load_dotenv
import os

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

# Number of messages to scrape from each channel
MESSAGE_LIMIT = 500

CHANNELS = [
    "lobelia4cosmetics",
    "tikvahpharma",
    "MedInEthio"
]