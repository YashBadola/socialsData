import sqlite3
import json
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path="socials.db"):
        self.db_path = db_path

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Initialize the database schema."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Personalities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personalities (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                system_prompt TEXT
            )
        ''')

        # Content table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT,
                text TEXT,
                source TEXT,
                FOREIGN KEY(personality_id) REFERENCES personalities(id)
            )
        ''')

        # QA Pairs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS qa_pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT,
                instruction TEXT,
                response TEXT,
                source TEXT,
                FOREIGN KEY(personality_id) REFERENCES personalities(id)
            )
        ''')

        conn.commit()
        conn.close()
        print(f"Database initialized at {self.db_path}")

    def sync_personality(self, personality_id, personality_dir):
        """Syncs a personality's processed data into the database."""
        personality_dir = Path(personality_dir)
        metadata_path = personality_dir / "metadata.json"
        data_path = personality_dir / "processed" / "data.jsonl"
        qa_path = personality_dir / "processed" / "qa.jsonl"

        if not metadata_path.exists():
            print(f"Metadata not found for {personality_id}")
            return

        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        conn = self.get_connection()
        cursor = conn.cursor()

        # Upsert Personality
        cursor.execute('''
            INSERT OR REPLACE INTO personalities (id, name, description, system_prompt)
            VALUES (?, ?, ?, ?)
        ''', (
            metadata.get("id"),
            metadata.get("name"),
            metadata.get("description"),
            metadata.get("system_prompt")
        ))

        # Clear existing data for this personality to avoid duplicates (simplest strategy)
        cursor.execute("DELETE FROM content WHERE personality_id = ?", (personality_id,))
        cursor.execute("DELETE FROM qa_pairs WHERE personality_id = ?", (personality_id,))

        # Insert Content
        if data_path.exists():
            with open(data_path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        cursor.execute('''
                            INSERT INTO content (personality_id, text, source)
                            VALUES (?, ?, ?)
                        ''', (personality_id, record.get("text"), record.get("source")))
                    except json.JSONDecodeError:
                        continue

        # Insert QA
        if qa_path.exists():
            with open(qa_path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        cursor.execute('''
                            INSERT INTO qa_pairs (personality_id, instruction, response, source)
                            VALUES (?, ?, ?, ?)
                        ''', (
                            personality_id,
                            record.get("instruction"),
                            record.get("response"),
                            record.get("source")
                        ))
                    except json.JSONDecodeError:
                        continue

        conn.commit()
        conn.close()
        print(f"Synced {personality_id} to database.")

    def query(self, sql):
        """Executes a read-only query."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            return columns, rows
        except sqlite3.Error as e:
            print(f"SQL Error: {e}")
            return [], []
        finally:
            conn.close()
