import os
import json
import logging
from pathlib import Path
from datetime import datetime

from telethon import TelegramClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE_NUMBER")

client = TelegramClient("session", API_ID, API_HASH)

CHANNELS = [
    "CheMed123",
    "lobelia4cosmetics",
    "tikvahpharma",
]

# Create directories
Path("logs").mkdir(exist_ok=True)
Path("data/raw/telegram_messages").mkdir(parents=True, exist_ok=True)
Path("data/raw/images").mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def scrape_channel(channel):
    print(f"\nScraping {channel}...")

    messages = []
    image_count = 0

    async for message in client.iter_messages(channel, limit=50):

        image_path = None

        # Download only first 20 images
        if message.photo and image_count < 20:

            img_dir = Path(f"data/raw/images/{channel}")
            img_dir.mkdir(parents=True, exist_ok=True)

            image_path = img_dir / f"{message.id}.jpg"

            try:
                await message.download_media(file=image_path)
                image_count += 1
            except Exception as e:
                logging.error(f"Image download failed ({channel}, {message.id}): {e}")

        messages.append({
            "message_id": message.id,
            "channel_name": channel,
            "message_date": message.date.isoformat() if message.date else None,
            "message_text": message.text,
            "views": message.views,
            "forwards": message.forwards,
            "has_media": message.photo is not None,
            "image_path": str(image_path) if image_path else None
        })

    # Save JSON
    date_folder = datetime.today().strftime("%Y-%m-%d")

    out_dir = Path(f"data/raw/telegram_messages/{date_folder}")
    out_dir.mkdir(parents=True, exist_ok=True)

    json_file = out_dir / f"{channel}.json"

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

    logging.info(
        f"{channel}: {len(messages)} messages scraped, {image_count} images downloaded."
    )

    print(f"Finished {channel}")
    print(f"   Messages: {len(messages)}")
    print(f"   Images:   {image_count}")
    print(f"   Saved:    {json_file}")


async def main():

    print("Connecting to Telegram...")
    await client.start(phone=PHONE)
    print("Connected!\n")

    for channel in CHANNELS:
        try:
            await scrape_channel(channel)
        except Exception as e:
            logging.error(f"Failed to scrape {channel}: {e}")
            print(f"Error scraping {channel}: {e}")

    print("\nAll channels finished!")


with client:
    client.loop.run_until_complete(main())