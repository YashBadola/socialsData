#!/usr/bin/env python3
import sqlite3
import json
import logging
from pathlib import Path
from socials_data.core.manager import PersonalityManager

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DB_PATH = Path("philosophers.db")

def setup_database(cursor):
    """Creates the necessary tables."""
    logging.info("Setting up database schema...")
    cursor.execute("DROP TABLE IF EXISTS content")
    cursor.execute("DROP TABLE IF EXISTS personalities")

    cursor.execute("""
        CREATE TABLE personalities (
            id TEXT PRIMARY KEY,
            name TEXT,
            description TEXT,
            system_prompt TEXT,
            license TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            personality_id TEXT,
            text TEXT,
            source TEXT,
            FOREIGN KEY (personality_id) REFERENCES personalities(id)
        )
    """)

def populate_database(cursor, manager):
    """Iterates through personalities and populates the database."""
    personalities = manager.list_personalities()
    logging.info(f"Found {len(personalities)} personalities.")

    for pid in personalities:
        logging.info(f"Processing {pid}...")

        # 1. Metadata
        try:
            meta = manager.get_metadata(pid)
            cursor.execute("""
                INSERT INTO personalities (id, name, description, system_prompt, license)
                VALUES (?, ?, ?, ?, ?)
            """, (
                meta.get("id"),
                meta.get("name"),
                meta.get("description"),
                meta.get("system_prompt"),
                meta.get("license")
            ))
        except Exception as e:
            logging.error(f"Failed to insert metadata for {pid}: {e}")
            continue

        # 2. Processed Content
        processed_file = manager.base_dir / pid / "processed" / "data.jsonl"
        if processed_file.exists():
            try:
                with open(processed_file, "r", encoding="utf-8") as f:
                    count = 0
                    for line in f:
                        try:
                            record = json.loads(line)
                            text = record.get("text")
                            source = record.get("source", "unknown")

                            if text:
                                cursor.execute("""
                                    INSERT INTO content (personality_id, text, source)
                                    VALUES (?, ?, ?)
                                """, (pid, text, source))
                                count += 1
                        except json.JSONDecodeError:
                            continue
                    logging.info(f"  Inserted {count} records.")
            except Exception as e:
                logging.error(f"Failed to read data for {pid}: {e}")
        else:
            logging.warning(f"  No processed data found for {pid}.")

def main():
    manager = PersonalityManager()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        setup_database(cursor)
        populate_database(cursor, manager)
        conn.commit()

    logging.info(f"Database successfully created at {DB_PATH.resolve()}")

if __name__ == "__main__":
    main()
