import sqlite3
import json
from pathlib import Path
from typing import Optional, List, Dict
from socials_data.core.manager import PersonalityManager

DB_PATH = Path("socials.db")

class DatabaseManager:
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DB_PATH
        self.manager = PersonalityManager()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Initialize the database schema."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Personalities Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS personalities (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                system_prompt TEXT
            )
        """)

        # Sources Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT,
                filename TEXT,
                path TEXT,
                FOREIGN KEY(personality_id) REFERENCES personalities(id),
                UNIQUE(personality_id, filename)
            )
        """)

        # Chunks Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id INTEGER,
                text TEXT,
                sequence_index INTEGER,
                FOREIGN KEY(source_id) REFERENCES sources(id)
            )
        """)

        # QA Pairs Table
        # Linking to source_id for now as strict chunk mapping is hard from decoupled JSONL files
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS qa_pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id INTEGER,
                instruction TEXT,
                response TEXT,
                FOREIGN KEY(source_id) REFERENCES sources(id)
            )
        """)

        conn.commit()
        conn.close()
        print(f"Database initialized at {self.db_path}")

    def sync_personality(self, personality_id: str):
        """Syncs a personality's metadata and processed data into the DB."""
        # 1. Get Metadata
        try:
            metadata = self.manager.get_metadata(personality_id)
        except FileNotFoundError:
            print(f"Personality {personality_id} not found.")
            return

        conn = self.get_connection()
        cursor = conn.cursor()

        # Insert Personality
        cursor.execute("""
            INSERT OR REPLACE INTO personalities (id, name, description, system_prompt)
            VALUES (?, ?, ?, ?)
        """, (
            metadata.get("id"),
            metadata.get("name"),
            metadata.get("description"),
            metadata.get("system_prompt")
        ))

        # 2. Process Data
        processed_dir = self.manager.base_dir / personality_id / "processed"
        raw_dir = self.manager.base_dir / personality_id / "raw"
        data_file = processed_dir / "data.jsonl"
        qa_file = processed_dir / "qa.jsonl"

        source_map = {} # filename -> source_id

        if data_file.exists():
            print(f"Syncing data from {data_file}...")
            with open(data_file, "r", encoding="utf-8") as f:
                for i, line in enumerate(f):
                    try:
                        record = json.loads(line)
                        filename = record.get("source", "unknown")
                        text = record.get("text", "")

                        # Ensure Source exists
                        # We use INSERT OR IGNORE and then SELECT to get ID, or just select first
                        cursor.execute("""
                            INSERT OR IGNORE INTO sources (personality_id, filename, path)
                            VALUES (?, ?, ?)
                        """, (personality_id, filename, str(raw_dir / filename)))

                        # Get source_id
                        if filename not in source_map:
                            cursor.execute("SELECT id FROM sources WHERE personality_id = ? AND filename = ?", (personality_id, filename))
                            row = cursor.fetchone()
                            if row:
                                source_map[filename] = row[0]

                        source_id = source_map.get(filename)

                        # Insert Chunk
                        if source_id:
                            cursor.execute("""
                                INSERT INTO chunks (source_id, text, sequence_index)
                                VALUES (?, ?, ?)
                            """, (source_id, text, i))

                    except json.JSONDecodeError:
                        continue

        # 3. Process QA
        if qa_file.exists():
            print(f"Syncing QA from {qa_file}...")
            with open(qa_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        filename = record.get("source", "unknown")
                        instruction = record.get("instruction", "")
                        response = record.get("response", "")

                        source_id = source_map.get(filename)

                        # If source wasn't found in data.jsonl (maybe QA generated separately?), try to find/create it
                        if not source_id:
                             cursor.execute("SELECT id FROM sources WHERE personality_id = ? AND filename = ?", (personality_id, filename))
                             row = cursor.fetchone()
                             if row:
                                 source_id = row[0]
                                 source_map[filename] = source_id

                        if source_id:
                            cursor.execute("""
                                INSERT INTO qa_pairs (source_id, instruction, response)
                                VALUES (?, ?, ?)
                            """, (source_id, instruction, response))

                    except json.JSONDecodeError:
                        continue

        conn.commit()
        conn.close()
        print(f"Synced {personality_id} to database.")

if __name__ == "__main__":
    # Test
    db = DatabaseManager()
    db.init_db()
