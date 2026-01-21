import sqlite3
from pathlib import Path
import json

DB_PATH = Path(__file__).parent.parent / "philosophers.db"

class Database:
    def __init__(self, db_path=None):
        self.db_path = db_path if db_path else DB_PATH
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

        # Personalities
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personalities (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                system_prompt TEXT
            )
        ''')

        # Documents
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT,
                filename TEXT,
                content TEXT,
                source_url TEXT,
                FOREIGN KEY(personality_id) REFERENCES personalities(id)
            )
        ''')

        # Chunks
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER,
                text TEXT,
                FOREIGN KEY(document_id) REFERENCES documents(id)
            )
        ''')

        # QA Pairs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS qa_pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chunk_id INTEGER,
                question TEXT,
                answer TEXT,
                FOREIGN KEY(chunk_id) REFERENCES chunks(id)
            )
        ''')

        self.conn.commit()
        self.close()

    def add_personality(self, p_id, name, description, system_prompt):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO personalities (id, name, description, system_prompt)
            VALUES (?, ?, ?, ?)
        ''', (p_id, name, description, system_prompt))
        self.conn.commit()
        self.close()

    def get_personality(self, p_id):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM personalities WHERE id = ?', (p_id,))
        row = cursor.fetchone()
        self.close()
        return dict(row) if row else None

    def add_document(self, personality_id, filename, content, source_url=None):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO documents (personality_id, filename, content, source_url)
            VALUES (?, ?, ?, ?)
        ''', (personality_id, filename, content, source_url))
        doc_id = cursor.lastrowid
        self.conn.commit()
        self.close()
        return doc_id

    def add_chunk(self, document_id, text):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO chunks (document_id, text)
            VALUES (?, ?)
        ''', (document_id, text))
        chunk_id = cursor.lastrowid
        self.conn.commit()
        self.close()
        return chunk_id

    def add_qa_pair(self, chunk_id, question, answer):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO qa_pairs (chunk_id, question, answer)
            VALUES (?, ?, ?)
        ''', (chunk_id, question, answer))
        self.conn.commit()
        self.close()
