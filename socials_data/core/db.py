import sqlite3
import json
from pathlib import Path

DEFAULT_DB_PATH = Path("socials.db")

class DatabaseManager:
    def __init__(self, db_path=None):
        self.db_path = Path(db_path) if db_path else DEFAULT_DB_PATH

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Creates the database tables if they do not exist."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Create personalities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personalities (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                system_prompt TEXT
            )
        ''')

        # Create content table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT,
                text TEXT,
                source TEXT,
                FOREIGN KEY(personality_id) REFERENCES personalities(id)
            )
        ''')

        # Create qa_pairs table
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
        """
        Syncs data from a personality directory into the database.
        personality_dir should be a Path object.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        personality_dir = Path(personality_dir)
        metadata_file = personality_dir / "metadata.json"

        if not metadata_file.exists():
            print(f"Error: No metadata found for {personality_id}")
            conn.close()
            return

        # 1. Update Personality Metadata
        with open(metadata_file, "r", encoding="utf-8") as f:
            meta = json.load(f)

        cursor.execute('''
            INSERT OR REPLACE INTO personalities (id, name, description, system_prompt)
            VALUES (?, ?, ?, ?)
        ''', (meta.get("id", personality_id), meta.get("name"), meta.get("description"), meta.get("system_prompt")))

        # 2. Clear existing content for this personality to avoid duplicates
        cursor.execute('DELETE FROM content WHERE personality_id = ?', (personality_id,))
        cursor.execute('DELETE FROM qa_pairs WHERE personality_id = ?', (personality_id,))

        # 3. Insert Content
        data_file = personality_dir / "processed" / "data.jsonl"
        if data_file.exists():
            with open(data_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        cursor.execute('''
                            INSERT INTO content (personality_id, text, source)
                            VALUES (?, ?, ?)
                        ''', (personality_id, record.get("text"), record.get("source")))
                    except json.JSONDecodeError:
                        continue

        # 4. Insert QA Pairs
        qa_file = personality_dir / "processed" / "qa.jsonl"
        if qa_file.exists():
            with open(qa_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        cursor.execute('''
                            INSERT INTO qa_pairs (personality_id, instruction, response, source)
                            VALUES (?, ?, ?, ?)
                        ''', (personality_id, record.get("instruction"), record.get("response"), record.get("source")))
                    except json.JSONDecodeError:
                        continue

        conn.commit()
        conn.close()
        print(f"Synced {personality_id} to database.")

    def query(self, sql_query):
        """Executes a raw SQL query and returns the results."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql_query)
            if sql_query.strip().upper().startswith("SELECT"):
                columns = [description[0] for description in cursor.description]
                results = cursor.fetchall()
                conn.close()
                return columns, results
            else:
                conn.commit()
                conn.close()
                return [], []
        except Exception as e:
            conn.close()
            raise e
