import os
import json
from datetime import datetime

from tqdm import tqdm
from telethon import TelegramClient
from telethon.errors import FloodWaitError

from config import API_ID, API_HASH, PHONE_NUMBER, CHANNELS, MESSAGE_LIMIT
from logger import logger

# =====================================================
# Telegram Client
# =====================================================

client = TelegramClient("telegram_session", API_ID, API_HASH)


# =====================================================
# Utilities
# =====================================================

def create_directory(path: str):
    os.makedirs(path, exist_ok=True)


# =====================================================
# Download Images
# =====================================================

async def download_image(message, channel_name: str):
    image_folder = os.path.join("data", "raw", "images", channel_name)
    create_directory(image_folder)

    image_path = os.path.join(image_folder, f"{message.id}.jpg")

    try:
        await client.download_media(message, file=image_path)
        return image_path

    except Exception as e:
        logger.error(f"Image download failed (msg {message.id}): {e}")
        return None


# =====================================================
# Save JSON
# =====================================================

def save_json(messages, channel_name: str):
    today = datetime.now().strftime("%Y-%m-%d")

    folder = os.path.join("data", "raw", "telegram_messages", today)
    create_directory(folder)

    json_path = os.path.join(folder, f"{channel_name}.json")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4, default=str)

    logger.info(f"Saved {len(messages)} messages → {json_path}")


# =====================================================
# Scrape Channel
# =====================================================

async def scrape_channel(channel_name: str):
    logger.info(f"Starting scraping: {channel_name}")

    messages_data = []

    try:
        # Step 1: collect messages
        messages = [
            msg async for msg in client.iter_messages(
                channel_name,
                limit=MESSAGE_LIMIT
            )
        ]

        # Step 2: process messages
        for message in tqdm(messages, desc=f"{channel_name}"):

            image_path = None

            if message.photo:
                image_path = await download_image(message, channel_name)

            record = {
                "message_id": message.id,
                "channel_name": channel_name,
                "message_date": str(message.date),
                "message_text": message.text if message.text else "",
                "views": message.views,
                "forwards": message.forwards,
                "has_media": bool(message.photo),
                "image_path": image_path
            }

            messages_data.append(record)

        save_json(messages_data, channel_name)

        logger.info(
            f"Finished {channel_name} | "
            f"Messages: {len(messages_data)}"
        )

    except FloodWaitError as e:
        logger.warning(
            f"Rate limit hit on {channel_name}. "
            f"Wait {e.seconds} seconds."
        )

    except Exception as e:
        logger.exception(f"Error scraping {channel_name}: {e}")


# =====================================================
# Main
# =====================================================

async def main():
    logger.info("Connecting to Telegram...")

    await client.start(phone=PHONE_NUMBER)

    logger.info("Connected successfully.")

    for channel in CHANNELS:
        await scrape_channel(channel)

    await client.disconnect()
    logger.info("All channels scraped successfully.")


# =====================================================
# Run
# =====================================================

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())