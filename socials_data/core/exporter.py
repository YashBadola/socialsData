import sqlite3
import json
from pathlib import Path
import logging

class SQLiteExporter:
    def __init__(self, personality_id, personality_dir):
        self.personality_id = personality_id
        self.personality_dir = Path(personality_dir)
        self.db_path = self.personality_dir / "processed" / "database.db"

    def export(self):
        """
        Exports metadata, content, and QA pairs to a SQLite database.
        """
        if not self.db_path.parent.exists():
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        self._create_tables(cursor)
        self._export_metadata(cursor)
        self._export_content(cursor)
        self._export_qa(cursor)

        conn.commit()
        conn.close()
        print(f"Database exported to {self.db_path}")

    def _create_tables(self, cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS personality (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                system_prompt TEXT,
                license TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT,
                text TEXT,
                source_file TEXT,
                FOREIGN KEY(personality_id) REFERENCES personality(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS qa_pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT,
                instruction TEXT,
                response TEXT,
                source_file TEXT,
                FOREIGN KEY(personality_id) REFERENCES personality(id)
            )
        """)

    def _export_metadata(self, cursor):
        meta_file = self.personality_dir / "metadata.json"
        if meta_file.exists():
            try:
                with open(meta_file, "r") as f:
                    meta = json.load(f)
                    cursor.execute("""
                        INSERT OR REPLACE INTO personality (id, name, description, system_prompt, license)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        meta.get("id", self.personality_id),
                        meta.get("name"),
                        meta.get("description"),
                        meta.get("system_prompt"),
                        meta.get("license")
                    ))
            except Exception as e:
                logging.error(f"Failed to export metadata: {e}")

    def _export_content(self, cursor):
        data_file = self.personality_dir / "processed" / "data.jsonl"
        if data_file.exists():
            try:
                with open(data_file, "r") as f:
                    # Clear existing content for this personality to avoid duplicates if re-running
                    cursor.execute("DELETE FROM content WHERE personality_id = ?", (self.personality_id,))

                    for line in f:
                        record = json.loads(line)
                        cursor.execute("""
                            INSERT INTO content (personality_id, text, source_file)
                            VALUES (?, ?, ?)
                        """, (
                            self.personality_id,
                            record.get("text"),
                            record.get("source")
                        ))
            except Exception as e:
                logging.error(f"Failed to export content: {e}")

    def _export_qa(self, cursor):
        qa_file = self.personality_dir / "processed" / "qa.jsonl"
        if qa_file.exists():
            try:
                with open(qa_file, "r") as f:
                    # Clear existing qa for this personality
                    cursor.execute("DELETE FROM qa_pairs WHERE personality_id = ?", (self.personality_id,))

                    for line in f:
                        record = json.loads(line)
                        cursor.execute("""
                            INSERT INTO qa_pairs (personality_id, instruction, response, source_file)
                            VALUES (?, ?, ?, ?)
                        """, (
                            self.personality_id,
                            record.get("instruction"),
                            record.get("response"),
                            record.get("source")
                        ))
            except Exception as e:
                logging.error(f"Failed to export QA pairs: {e}")
