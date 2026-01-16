import sqlite3
import json
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path="socials.db"):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()

        # Philosophers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS philosophers (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                license TEXT,
                system_prompt TEXT
            )
        """)

        # Works/Sources table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS works (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                philosopher_id TEXT NOT NULL,
                title TEXT,
                type TEXT,
                url TEXT,
                FOREIGN KEY (philosopher_id) REFERENCES philosophers(id) ON DELETE CASCADE
            )
        """)

        # Segments (Processed Text) table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS segments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                philosopher_id TEXT NOT NULL,
                text TEXT NOT NULL,
                source_filename TEXT,
                FOREIGN KEY (philosopher_id) REFERENCES philosophers(id) ON DELETE CASCADE
            )
        """)

        # QA Pairs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS qa_pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                philosopher_id TEXT NOT NULL,
                instruction TEXT NOT NULL,
                response TEXT NOT NULL,
                source_segment_id INTEGER,
                FOREIGN KEY (philosopher_id) REFERENCES philosophers(id) ON DELETE CASCADE,
                FOREIGN KEY (source_segment_id) REFERENCES segments(id) ON DELETE SET NULL
            )
        """)

        self.conn.commit()

    def add_philosopher(self, metadata):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO philosophers (id, name, description, license, system_prompt)
            VALUES (?, ?, ?, ?, ?)
        """, (
            metadata['id'],
            metadata['name'],
            metadata.get('description', ''),
            metadata.get('license', ''),
            metadata.get('system_prompt', '')
        ))

        # Add sources
        for source in metadata.get('sources', []):
            cursor.execute("""
                INSERT INTO works (philosopher_id, title, type, url)
                VALUES (?, ?, ?, ?)
            """, (
                metadata['id'],
                source.get('title'),
                source.get('type'),
                source.get('url')
            ))

        self.conn.commit()

    def add_segments(self, philosopher_id, jsonl_path):
        cursor = self.conn.cursor()
        path = Path(jsonl_path)
        if not path.exists():
            return

        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    record = json.loads(line)
                    text = record.get('text')
                    source = record.get('source')
                    if text:
                        cursor.execute("""
                            INSERT INTO segments (philosopher_id, text, source_filename)
                            VALUES (?, ?, ?)
                        """, (philosopher_id, text, source))
                except json.JSONDecodeError:
                    continue
        self.conn.commit()

    def add_qa_pairs(self, philosopher_id, jsonl_path):
        cursor = self.conn.cursor()
        path = Path(jsonl_path)
        if not path.exists():
            return

        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    record = json.loads(line)
                    instruction = record.get('instruction')
                    response = record.get('response')
                    # Note: linking to exact segment is hard without more metadata in jsonl,
                    # so we leave source_segment_id null for now or infer it if possible.
                    if instruction and response:
                        cursor.execute("""
                            INSERT INTO qa_pairs (philosopher_id, instruction, response)
                            VALUES (?, ?, ?)
                        """, (philosopher_id, instruction, response))
                except json.JSONDecodeError:
                    continue
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
