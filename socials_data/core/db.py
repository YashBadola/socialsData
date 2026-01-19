import sqlite3
from pathlib import Path
import json

DB_PATH = Path(__file__).parent.parent / "philosophers.db"

class Database:
    def __init__(self, db_path=None):
        self.db_path = db_path if db_path else DB_PATH
        self.conn = None

    def connect(self):
        if not self.conn:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def init_db(self):
        with self:
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

    def add_personality(self, p_id, name, description, system_prompt):
        # Auto-connect if not connected, allowing persistent usage if desired
        close_after = False
        if not self.conn:
            self.connect()
            close_after = True

        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO personalities (id, name, description, system_prompt)
                VALUES (?, ?, ?, ?)
            ''', (p_id, name, description, system_prompt))
            self.conn.commit()
        finally:
            if close_after:
                self.close()

    def get_personality(self, p_id):
        close_after = False
        if not self.conn:
            self.connect()
            close_after = True

        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM personalities WHERE id = ?', (p_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            if close_after:
                self.close()

    def add_document(self, personality_id, filename, content, source_url=None):
        close_after = False
        if not self.conn:
            self.connect()
            close_after = True

        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO documents (personality_id, filename, content, source_url)
                VALUES (?, ?, ?, ?)
            ''', (personality_id, filename, content, source_url))
            doc_id = cursor.lastrowid
            self.conn.commit()
            return doc_id
        finally:
            if close_after:
                self.close()

    def add_chunk(self, document_id, text):
        close_after = False
        if not self.conn:
            self.connect()
            close_after = True

        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO chunks (document_id, text)
                VALUES (?, ?)
            ''', (document_id, text))
            chunk_id = cursor.lastrowid
            self.conn.commit()
            return chunk_id
        finally:
            if close_after:
                self.close()

    def add_qa_pair(self, chunk_id, question, answer):
        close_after = False
        if not self.conn:
            self.connect()
            close_after = True

        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO qa_pairs (chunk_id, question, answer)
                VALUES (?, ?, ?)
            ''', (chunk_id, question, answer))
            self.conn.commit()
        finally:
            if close_after:
                self.close()

    def clear_documents(self, personality_id):
        close_after = False
        if not self.conn:
            self.connect()
            close_after = True

        try:
            cursor = self.conn.cursor()
            # Delete chunks and qa_pairs associated with documents of this personality
            # This requires finding document IDs first or cascading delete if enabled (but SQLite needs PRAGMA foreign_keys = ON)
            # Let's do it manually to be safe.
            cursor.execute("SELECT id FROM documents WHERE personality_id = ?", (personality_id,))
            doc_ids = [row[0] for row in cursor.fetchall()]

            if doc_ids:
                # Placeholders for IN clause
                placeholders = ', '.join('?' * len(doc_ids))

                # Delete QA pairs (linked to chunks)
                cursor.execute(f"DELETE FROM qa_pairs WHERE chunk_id IN (SELECT id FROM chunks WHERE document_id IN ({placeholders}))", doc_ids)

                # Delete Chunks
                cursor.execute(f"DELETE FROM chunks WHERE document_id IN ({placeholders})", doc_ids)

                # Delete Documents
                cursor.execute("DELETE FROM documents WHERE personality_id = ?", (personality_id,))

            self.conn.commit()
        finally:
            if close_after:
                self.close()
