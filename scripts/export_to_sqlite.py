#!/usr/bin/env python3
import sqlite3
import json
from pathlib import Path
from socials_data.core.manager import PersonalityManager

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    except sqlite3.Error as e:
        print(e)
    return None

def create_tables(conn):
    create_personalities_table = """
    CREATE TABLE IF NOT EXISTS personalities (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        system_prompt TEXT,
        license TEXT
    );
    """

    create_content_table = """
    CREATE TABLE IF NOT EXISTS content (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        personality_id TEXT NOT NULL,
        text TEXT NOT NULL,
        source TEXT,
        FOREIGN KEY (personality_id) REFERENCES personalities (id) ON DELETE CASCADE
    );
    """

    create_qa_table = """
    CREATE TABLE IF NOT EXISTS qa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        personality_id TEXT NOT NULL,
        instruction TEXT NOT NULL,
        response TEXT NOT NULL,
        FOREIGN KEY (personality_id) REFERENCES personalities (id) ON DELETE CASCADE
    );
    """

    try:
        c = conn.cursor()
        c.execute(create_personalities_table)
        c.execute(create_content_table)
        c.execute(create_qa_table)
    except sqlite3.Error as e:
        print(e)

def export_data(db_file):
    manager = PersonalityManager()
    personalities = manager.list_personalities()

    conn = create_connection(db_file)
    if conn is None:
        print("Error! cannot create the database connection.")
        return

    create_tables(conn)
    cur = conn.cursor()

    print(f"Exporting {len(personalities)} personalities to {db_file}...")

    # Clear existing data to ensure idempotency
    cur.execute("DELETE FROM qa")
    cur.execute("DELETE FROM content")
    cur.execute("DELETE FROM personalities")

    for p_id in personalities:
        print(f"Processing {p_id}...")

        # 1. Metadata
        try:
            metadata = manager.get_metadata(p_id)
            cur.execute("""
                INSERT INTO personalities (id, name, description, system_prompt, license)
                VALUES (?, ?, ?, ?, ?)
            """, (
                metadata.get("id"),
                metadata.get("name"),
                metadata.get("description"),
                metadata.get("system_prompt"),
                metadata.get("license")
            ))
        except Exception as e:
            print(f"Error reading metadata for {p_id}: {e}")
            continue

        # 2. Content (processed/data.jsonl)
        data_path = manager.base_dir / p_id / "processed" / "data.jsonl"
        if data_path.exists():
            with open(data_path, 'r') as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        cur.execute("""
                            INSERT INTO content (personality_id, text, source)
                            VALUES (?, ?, ?)
                        """, (
                            p_id,
                            record.get("text"),
                            record.get("source")
                        ))
                    except json.JSONDecodeError:
                        pass

        # 3. QA (processed/qa.jsonl)
        qa_path = manager.base_dir / p_id / "processed" / "qa.jsonl"
        if qa_path.exists():
            with open(qa_path, 'r') as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        cur.execute("""
                            INSERT INTO qa (personality_id, instruction, response)
                            VALUES (?, ?, ?)
                        """, (
                            p_id,
                            record.get("instruction"),
                            record.get("response")
                        ))
                    except json.JSONDecodeError:
                        pass

    conn.commit()
    conn.close()
    print("Export complete.")

if __name__ == "__main__":
    export_data("socials_data.db")
