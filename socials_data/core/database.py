import sqlite3
import json
from pathlib import Path
import logging

class SocialsDatabase:
    def __init__(self, db_path="socials.db"):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        if self.conn:
            self.conn.close()

    def init_db(self):
        self.connect()
        cursor = self.conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personalities (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT,
                text TEXT,
                source TEXT,
                FOREIGN KEY(personality_id) REFERENCES personalities(id)
            )
        ''')

        self.conn.commit()
        self.close()

    def sync_personality(self, personality_id, personality_dir):
        self.connect()
        cursor = self.conn.cursor()
        personality_dir = Path(personality_dir)
        metadata_file = personality_dir / "metadata.json"
        data_file = personality_dir / "processed" / "data.jsonl"

        if not metadata_file.exists():
            logging.error(f"Metadata file not found for {personality_id}")
            self.close()
            return

        with open(metadata_file, "r", encoding="utf-8") as f:
            meta = json.load(f)
            name = meta.get("name", "Unknown")
            description = meta.get("description", "")

        cursor.execute('''
            INSERT OR REPLACE INTO personalities (id, name, description)
            VALUES (?, ?, ?)
        ''', (personality_id, name, description))

        if data_file.exists():
            # Clear existing content for this personality to avoid duplicates on re-sync
            cursor.execute('DELETE FROM content WHERE personality_id = ?', (personality_id,))

            with open(data_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        text = record.get("text", "")
                        source = record.get("source", "unknown")
                        if text:
                            cursor.execute('''
                                INSERT INTO content (personality_id, text, source)
                                VALUES (?, ?, ?)
                            ''', (personality_id, text, source))
                    except json.JSONDecodeError:
                        logging.warning(f"Skipping invalid JSON line in {data_file}")
                        continue

        self.conn.commit()
        self.close()
        print(f"Synced {personality_id} to database.")

    def query(self, query_text):
        self.connect()
        cursor = self.conn.cursor()
        # Simple LIKE query
        search_pattern = f"%{query_text}%"
        cursor.execute('''
            SELECT p.name, c.text, c.source
            FROM content c
            JOIN personalities p ON c.personality_id = p.id
            WHERE c.text LIKE ?
        ''', (search_pattern,))

        results = cursor.fetchall()
        self.close()
        return results
