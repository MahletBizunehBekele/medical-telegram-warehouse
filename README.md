# Medical Telegram Warehouse

## Overview
This project builds an ELT pipeline for collecting, transforming, and analyzing data from Ethiopian medical Telegram channels.

## Technologies
- Python
- Telethon
- PostgreSQL
- dbt

## Project Structure
- data/raw/telegram_messages
- data/raw/images
- src/
- medical_warehouse/

## Setup

pip install -r requirements.txt

Create a `.env` file:

API_ID=
API_HASH=
PHONE_NUMBER=

Run:

python src/scraper.py
python src/load_raw.py

cd medical_warehouse

dbt run
dbt test
dbt docs generate