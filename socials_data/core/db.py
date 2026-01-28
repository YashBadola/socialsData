import sqlite3
import json
import logging
from pathlib import Path
from socials_data.core.manager import PersonalityManager

DB_PATH = Path("socials.db")

class DatabaseManager:
    def __init__(self, db_path=None):
        self.db_path = db_path if db_path else DB_PATH
        self.personality_manager = PersonalityManager()

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

        # Content table (Raw text chunks)
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

    def sync_personality(self, personality_id):
        """
        Syncs data from processed JSONL files into the database.
        This operation replaces existing data for the given personality.
        """
        try:
            meta = self.personality_manager.get_metadata(personality_id)
        except FileNotFoundError:
            print(f"Personality {personality_id} not found.")
            return

        conn = self.get_connection()
        cursor = conn.cursor()

        # 1. Update/Insert Personality Metadata
        cursor.execute('''
            INSERT OR REPLACE INTO personalities (id, name, description, system_prompt)
            VALUES (?, ?, ?, ?)
        ''', (meta['id'], meta['name'], meta.get('description', ''), meta.get('system_prompt', '')))

        # 2. Clear existing content and QA for this personality to ensure fresh sync
        cursor.execute('DELETE FROM content WHERE personality_id = ?', (personality_id,))
        cursor.execute('DELETE FROM qa_pairs WHERE personality_id = ?', (personality_id,))

        # 3. Load Content
        data_file = self.personality_manager.base_dir / personality_id / "processed" / "data.jsonl"
        if data_file.exists():
            with open(data_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        cursor.execute('''
                            INSERT INTO content (personality_id, text, source)
                            VALUES (?, ?, ?)
                        ''', (personality_id, record.get('text'), record.get('source')))
                    except json.JSONDecodeError:
                        continue

        # 4. Load QA
        qa_file = self.personality_manager.base_dir / personality_id / "processed" / "qa.jsonl"
        if qa_file.exists():
            with open(qa_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        cursor.execute('''
                            INSERT INTO qa_pairs (personality_id, instruction, response, source)
                            VALUES (?, ?, ?, ?)
                        ''', (personality_id, record.get('instruction'), record.get('response'), record.get('source')))
                    except json.JSONDecodeError:
                        continue

        conn.commit()
        conn.close()
        print(f"Synced {personality_id} to database.")

    def query(self, sql_query):
        """Executes a raw SQL query and returns results."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql_query)
            if sql_query.strip().upper().startswith("SELECT"):
                results = cursor.fetchall()
                # Get column names
                columns = [description[0] for description in cursor.description]
                return columns, results
            else:
                conn.commit()
                return [], []
        except sqlite3.Error as e:
            return None, f"SQL Error: {e}"
        finally:
            conn.close()
