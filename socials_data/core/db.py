import sqlite3
from pathlib import Path
import json

DB_PATH = Path(__file__).parent.parent / "philosophers.db"

class Database:
    def __init__(self, db_path=None):
        self.db_path = db_path or DB_PATH
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()

        # Personalities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personalities (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                system_prompt TEXT,
                license TEXT
            )
        ''')

        # Documents table (Raw data)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT,
                filename TEXT,
                content TEXT,
                source_url TEXT,
                type TEXT,
                FOREIGN KEY(personality_id) REFERENCES personalities(id)
            )
        ''')

        # Chunks table (Processed text)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER,
                text TEXT,
                chunk_index INTEGER,
                FOREIGN KEY(document_id) REFERENCES documents(id)
            )
        ''')

        # QA Pairs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS qa_pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chunk_id INTEGER,
                instruction TEXT,
                response TEXT,
                model_used TEXT,
                FOREIGN KEY(chunk_id) REFERENCES chunks(id)
            )
        ''')

        self.conn.commit()

    def add_personality(self, p_id, name, description="", system_prompt="", license="Unknown"):
        try:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO personalities (id, name, description, system_prompt, license) VALUES (?, ?, ?, ?, ?)",
                    (p_id, name, description, system_prompt, license)
                )
            return p_id
        except sqlite3.IntegrityError:
            raise ValueError(f"Personality '{p_id}' already exists.")

    def get_personality(self, p_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM personalities WHERE id = ?", (p_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

    def list_personalities(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name FROM personalities")
        return [dict(row) for row in cursor.fetchall()]

    def add_document(self, personality_id, filename, content, source_url="", doc_type="text"):
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO documents (personality_id, filename, content, source_url, type) VALUES (?, ?, ?, ?, ?)",
                (personality_id, filename, content, source_url, doc_type)
            )
            return cursor.lastrowid

    def get_documents(self, personality_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM documents WHERE personality_id = ?", (personality_id,))
        return [dict(row) for row in cursor.fetchall()]

    def add_chunk(self, document_id, text, chunk_index):
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO chunks (document_id, text, chunk_index) VALUES (?, ?, ?)",
                (document_id, text, chunk_index)
            )
            return cursor.lastrowid

    def get_chunks(self, document_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM chunks WHERE document_id = ? ORDER BY chunk_index", (document_id,))
        return [dict(row) for row in cursor.fetchall()]

    def clear_chunks(self, document_id):
        with self.conn:
            self.conn.execute("DELETE FROM chunks WHERE document_id = ?", (document_id,))

    def add_qa_pair(self, chunk_id, instruction, response, model_used="gpt-4o"):
        with self.conn:
            self.conn.execute(
                "INSERT INTO qa_pairs (chunk_id, instruction, response, model_used) VALUES (?, ?, ?, ?)",
                (chunk_id, instruction, response, model_used)
            )

    def get_qa_pairs(self, personality_id):
        cursor = self.conn.cursor()
        query = '''
            SELECT qa.instruction, qa.response
            FROM qa_pairs qa
            JOIN chunks c ON qa.chunk_id = c.id
            JOIN documents d ON c.document_id = d.id
            WHERE d.personality_id = ?
        '''
        cursor.execute(query, (personality_id,))
        return [dict(row) for row in cursor.fetchall()]

    def close(self):
        self.conn.close()
