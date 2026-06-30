import os
import json
import pandas as pd
import psycopg2
from datetime import datetime

# =========================
# DB CONFIG
# =========================

DB_CONFIG = {
    "dbname": "medical_warehouse",
    "user": "postgres",
    "password": "21@21$",
    "host": "localhost",
    "port": 5432
}

DATA_PATH = "data/raw/telegram_messages"


# =========================
# CONNECT DB
# =========================

def get_connection():
    return psycopg2.connect(**DB_CONFIG)


# =========================
# LOAD JSON FILES
# =========================

def load_json_files():
    all_data = []

    for root, dirs, files in os.walk(DATA_PATH):
        for file in files:
            if file.endswith(".json"):
                path = os.path.join(root, file)

                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    all_data.extend(data)

    return all_data


# =========================
# INSERT INTO POSTGRES
# =========================

def insert_data(records):
    conn = get_connection()
    cur = conn.cursor()

    for r in records:
       cur.execute("""
    INSERT INTO raw.telegram_messages (
        message_id,
        channel_name,
        message_date,
        message_text,
        views,
        forwards,
        has_image,
        image_path
    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
""", (
    r.get("message_id"),
    r.get("channel_name"),
    r.get("message_date"),
    r.get("message_text", ""),
    r.get("views", 0),
    r.get("forwards", 0),
    r.get("has_media", False),   # 👈 THIS IS THE FIX
    r.get("image_path")
))

    conn.commit()
    cur.close()
    conn.close()


# =========================
# RUN PIPELINE
# =========================

if __name__ == "__main__":
    print("Loading JSON files...")
    data = load_json_files()

    print(f"Total records: {len(data)}")

    print("Inserting into PostgreSQL...")
    insert_data(data)

    print("Done!")