import sqlite3
from pathlib import Path
import json

DB_PATH = Path(__file__).parent.parent / "philosophers.db"

class Database:
    def __init__(self, db_path=None):
        self.db_path = db_path or DB_PATH
        self._init_db()

    def _init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # Personalities Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personalities (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                system_prompt TEXT,
                license TEXT
            )
        ''')

        # Sources/Documents Table
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

        # Chunks Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER,
                text TEXT,
                chunk_index INTEGER,
                FOREIGN KEY(document_id) REFERENCES documents(id)
            )
        ''')

        # Q&A Pairs Table
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

        conn.commit()
        conn.close()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def add_personality(self, pid, name, description, system_prompt, license):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO personalities (id, name, description, system_prompt, license)
                VALUES (?, ?, ?, ?, ?)
            ''', (pid, name, description, system_prompt, license))
            conn.commit()
        finally:
            conn.close()

    def get_personality(self, pid):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM personalities WHERE id = ?', (pid,))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "system_prompt": row[3],
                    "license": row[4]
                }
            return None
        finally:
            conn.close()

    def list_personalities(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT id, name FROM personalities')
            return [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
        finally:
            conn.close()

    def add_document(self, personality_id, filename, content, source_url=None, doc_type="text"):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO documents (personality_id, filename, content, source_url, type)
                VALUES (?, ?, ?, ?, ?)
            ''', (personality_id, filename, content, source_url, doc_type))
            doc_id = cursor.lastrowid
            conn.commit()
            return doc_id
        finally:
            conn.close()

    def get_documents(self, personality_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM documents WHERE personality_id = ?', (personality_id,))
            return cursor.fetchall()
        finally:
            conn.close()

    def add_chunk(self, document_id, text, chunk_index):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO chunks (document_id, text, chunk_index)
                VALUES (?, ?, ?)
            ''', (document_id, text, chunk_index))
            chunk_id = cursor.lastrowid
            conn.commit()
            return chunk_id
        finally:
            conn.close()

    def add_qa_pair(self, chunk_id, instruction, response, model_used="gpt-4o"):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO qa_pairs (chunk_id, instruction, response, model_used)
                VALUES (?, ?, ?, ?)
            ''', (chunk_id, instruction, response, model_used))
            qa_id = cursor.lastrowid
            conn.commit()
            return qa_id
        finally:
            conn.close()
