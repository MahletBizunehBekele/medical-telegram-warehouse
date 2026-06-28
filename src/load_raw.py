import os
import json
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_USER = (os.getenv("DB_USER"))
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# -------------------------------
# PostgreSQL Connection
# -------------------------------


engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# -------------------------------
# Read all JSON files
# -------------------------------

json_dir = Path("data/raw/telegram_messages")

all_data = []

for json_file in json_dir.rglob("*.json"):

    print(f"Loading {json_file}")

    with open(json_file, "r", encoding="utf-8") as f:
        messages = json.load(f)

    all_data.extend(messages)

df = pd.DataFrame(all_data)

print(f"Loaded {len(df)} messages.")

# -------------------------------
# Convert date column
# -------------------------------

df["message_date"] = pd.to_datetime(df["message_date"])

# -------------------------------
# Insert into PostgreSQL
# -------------------------------

df.to_sql(
    "telegram_messages",
    engine,
    schema="raw",
    if_exists="append",
    index=False
)

print("Done!")