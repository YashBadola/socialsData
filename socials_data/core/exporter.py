import sqlite3
import json
from pathlib import Path

class SQLiteExporter:
    def __init__(self, personality_dir):
        self.personality_dir = Path(personality_dir)
        self.processed_dir = self.personality_dir / "processed"
        self.db_path = self.processed_dir / "database.db"

    def export(self):
        """
        Exports the processed data and metadata to a SQLite database.
        """
        if not self.processed_dir.exists():
            raise FileNotFoundError(f"Processed directory not found: {self.processed_dir}")

        data_file = self.processed_dir / "data.jsonl"
        metadata_file = self.personality_dir / "metadata.json"

        if not data_file.exists():
            raise FileNotFoundError(f"Processed data not found: {data_file}. Run 'process' first.")

        # Connect to SQLite DB
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create Tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personality (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                system_prompt TEXT,
                license TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS writings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                source TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS qa_pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                instruction TEXT,
                response TEXT,
                source TEXT
            )
        ''')

        # Insert Metadata
        if metadata_file.exists():
            with open(metadata_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
                cursor.execute('''
                    INSERT OR REPLACE INTO personality (id, name, description, system_prompt, license)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    meta.get("id"),
                    meta.get("name"),
                    meta.get("description"),
                    meta.get("system_prompt"),
                    meta.get("license")
                ))

        # Insert Writings
        # We clear existing data to avoid duplicates on re-run
        cursor.execute('DELETE FROM writings')

        with open(data_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    record = json.loads(line)
                    text = record.get("text")
                    source = record.get("source")
                    if text:
                        cursor.execute('INSERT INTO writings (text, source) VALUES (?, ?)', (text, source))
                except json.JSONDecodeError:
                    continue

        # Insert QA Pairs if available
        qa_file = self.processed_dir / "qa.jsonl"
        cursor.execute('DELETE FROM qa_pairs')
        if qa_file.exists():
            with open(qa_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        instruction = record.get("instruction")
                        response = record.get("response")
                        source = record.get("source")
                        if instruction and response:
                            cursor.execute('INSERT INTO qa_pairs (instruction, response, source) VALUES (?, ?, ?)', (instruction, response, source))
                    except json.JSONDecodeError:
                        continue

        conn.commit()
        conn.close()
        return self.db_path
