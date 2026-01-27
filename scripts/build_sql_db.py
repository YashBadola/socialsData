import sqlite3
import json
import os
from pathlib import Path
from socials_data.core.manager import PersonalityManager

def build_database(db_path="socials_data/philosophers.db"):
    print(f"Building database at {db_path}...")

    # Ensure directory exists
    db_path_obj = Path(db_path)
    db_path_obj.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS philosophers (
        id TEXT PRIMARY KEY,
        name TEXT,
        description TEXT,
        system_prompt TEXT,
        license TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS works (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        philosopher_id TEXT,
        text TEXT,
        source TEXT,
        FOREIGN KEY(philosopher_id) REFERENCES philosophers(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS qa_pairs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        philosopher_id TEXT,
        instruction TEXT,
        response TEXT,
        source TEXT,
        FOREIGN KEY(philosopher_id) REFERENCES philosophers(id)
    )
    """)

    # Clear existing data to avoid duplicates if run multiple times
    cursor.execute("DELETE FROM philosophers")
    cursor.execute("DELETE FROM works")
    cursor.execute("DELETE FROM qa_pairs")

    manager = PersonalityManager()
    personalities = manager.list_personalities()

    for p_id in personalities:
        print(f"Processing {p_id}...")

        # Metadata
        try:
            meta = manager.get_metadata(p_id)
            cursor.execute("""
            INSERT INTO philosophers (id, name, description, system_prompt, license)
            VALUES (?, ?, ?, ?, ?)
            """, (
                meta.get("id"),
                meta.get("name"),
                meta.get("description"),
                meta.get("system_prompt"),
                meta.get("license")
            ))
        except Exception as e:
            print(f"Error reading metadata for {p_id}: {e}")
            continue

        p_dir = manager.base_dir / p_id
        processed_dir = p_dir / "processed"

        # Works (data.jsonl)
        data_file = processed_dir / "data.jsonl"
        if data_file.exists():
            with open(data_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        cursor.execute("""
                        INSERT INTO works (philosopher_id, text, source)
                        VALUES (?, ?, ?)
                        """, (p_id, record.get("text"), record.get("source")))
                    except json.JSONDecodeError:
                        continue

        # QA Pairs (qa.jsonl)
        qa_file = processed_dir / "qa.jsonl"
        if qa_file.exists():
            with open(qa_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        cursor.execute("""
                        INSERT INTO qa_pairs (philosopher_id, instruction, response, source)
                        VALUES (?, ?, ?, ?)
                        """, (
                            p_id,
                            record.get("instruction"),
                            record.get("response"),
                            record.get("source")
                        ))
                    except json.JSONDecodeError:
                        continue

    conn.commit()
    conn.close()
    print("Database build complete.")

if __name__ == "__main__":
    build_database()
