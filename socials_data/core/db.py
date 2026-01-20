import sqlite3
from pathlib import Path
import json

class DBManager:
    def __init__(self, db_path=None):
        if db_path is None:
            self.db_path = Path(__file__).parent.parent / "socials.db"
        else:
            self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()

    def create_tables(self):
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

        # Documents table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT NOT NULL,
                filename TEXT NOT NULL,
                content TEXT,
                source_url TEXT,
                source_type TEXT,
                title TEXT,
                FOREIGN KEY (personality_id) REFERENCES personalities (id)
            )
        ''')

        # Chunks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                chunk_index INTEGER,
                FOREIGN KEY (document_id) REFERENCES documents (id)
            )
        ''')

        # QA Pairs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS qa_pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chunk_id INTEGER,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                model_used TEXT,
                source_text TEXT,
                FOREIGN KEY (chunk_id) REFERENCES chunks (id)
            )
        ''')

        self.conn.commit()

    def add_personality(self, p_id, name, description="", system_prompt="", license=""):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO personalities (id, name, description, system_prompt, license)
            VALUES (?, ?, ?, ?, ?)
        ''', (p_id, name, description, system_prompt, license))
        self.conn.commit()

    def get_personality(self, p_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM personalities WHERE id = ?', (p_id,))
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

    def add_document(self, personality_id, filename, content, source_url="", source_type="", title=""):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO documents (personality_id, filename, content, source_url, source_type, title)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (personality_id, filename, content, source_url, source_type, title))
        self.conn.commit()
        return cursor.lastrowid

    def get_document_by_filename(self, personality_id, filename):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM documents WHERE personality_id = ? AND filename = ?
        ''', (personality_id, filename))
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "personality_id": row[1],
                "filename": row[2],
                "content": row[3],
                "source_url": row[4],
                "source_type": row[5],
                "title": row[6]
            }
        return None

    def add_chunk(self, document_id, text, chunk_index):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO chunks (document_id, text, chunk_index)
            VALUES (?, ?, ?)
        ''', (document_id, text, chunk_index))
        self.conn.commit()
        return cursor.lastrowid

    def add_qa_pair(self, chunk_id, question, answer, model_used="", source_text=""):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO qa_pairs (chunk_id, question, answer, model_used, source_text)
            VALUES (?, ?, ?, ?, ?)
        ''', (chunk_id, question, answer, model_used, source_text))
        self.conn.commit()
        return cursor.lastrowid

    def list_personalities(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id FROM personalities')
        return [row[0] for row in cursor.fetchall()]

    def close(self):
        self.conn.close()
