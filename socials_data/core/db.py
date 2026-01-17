import sqlite3
from pathlib import Path
import json
from typing import List, Dict, Optional, Any

DB_PATH = Path(__file__).parent.parent / "philosophers.db"

class Database:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.conn = None
        self.init_db()

    def get_connection(self):
        if not self.conn:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        return self.conn

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # Personalities Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personalities (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                system_prompt TEXT,
                metadata TEXT
            )
        ''')

        # Documents Table (Raw Sources)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT NOT NULL,
                filename TEXT NOT NULL,
                content TEXT,
                source_url TEXT,
                FOREIGN KEY (personality_id) REFERENCES personalities (id)
            )
        ''')

        # Chunks Table (Processed Text)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                chunk_index INTEGER,
                FOREIGN KEY (document_id) REFERENCES documents (id)
            )
        ''')

        # QA Pairs Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS qa_pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chunk_id INTEGER,
                personality_id TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                source TEXT,
                FOREIGN KEY (chunk_id) REFERENCES chunks (id),
                FOREIGN KEY (personality_id) REFERENCES personalities (id)
            )
        ''')

        conn.commit()

    def add_personality(self, p_id: str, name: str, description: str, system_prompt: str, metadata: Dict = None):
        conn = self.get_connection()
        cursor = conn.cursor()
        meta_json = json.dumps(metadata) if metadata else "{}"
        try:
            cursor.execute('''
                INSERT INTO personalities (id, name, description, system_prompt, metadata)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    name=excluded.name,
                    description=excluded.description,
                    system_prompt=excluded.system_prompt,
                    metadata=excluded.metadata
            ''', (p_id, name, description, system_prompt, meta_json))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def get_personality(self, p_id: str) -> Optional[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM personalities WHERE id = ?', (p_id,))
        row = cursor.fetchone()
        if row:
            d = dict(row)
            d['metadata'] = json.loads(d['metadata']) if d['metadata'] else {}
            return d
        return None

    def list_personalities(self) -> List[str]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM personalities')
        return [row['id'] for row in cursor.fetchall()]

    def add_document(self, personality_id: str, filename: str, content: str, source_url: str = None) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO documents (personality_id, filename, content, source_url)
            VALUES (?, ?, ?, ?)
        ''', (personality_id, filename, content, source_url))
        conn.commit()
        return cursor.lastrowid

    def get_documents(self, personality_id: str) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM documents WHERE personality_id = ?', (personality_id,))
        return [dict(row) for row in cursor.fetchall()]

    def add_chunk(self, document_id: int, text: str, index: int) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO chunks (document_id, text, chunk_index)
            VALUES (?, ?, ?)
        ''', (document_id, text, index))
        conn.commit()
        return cursor.lastrowid

    def add_qa_pair(self, personality_id: str, question: str, answer: str, source: str, chunk_id: int = None):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO qa_pairs (personality_id, question, answer, source, chunk_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (personality_id, question, answer, source, chunk_id))
        conn.commit()

    def get_qa_pairs(self, personality_id: str) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM qa_pairs WHERE personality_id = ?', (personality_id,))
        return [dict(row) for row in cursor.fetchall()]

    def clear_personality_data(self, personality_id: str):
        """Clears documents, chunks, and QA pairs for a personality (for re-processing)."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # We need to find documents first to delete chunks
        cursor.execute('SELECT id FROM documents WHERE personality_id = ?', (personality_id,))
        doc_ids = [row['id'] for row in cursor.fetchall()]

        if doc_ids:
            doc_ids_str = ','.join(map(str, doc_ids))
            cursor.execute(f'DELETE FROM chunks WHERE document_id IN ({doc_ids_str})')

        cursor.execute('DELETE FROM qa_pairs WHERE personality_id = ?', (personality_id,))
        cursor.execute('DELETE FROM documents WHERE personality_id = ?', (personality_id,))
        conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
