import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Optional, Any

DB_PATH = Path(__file__).parent.parent.parent / "philosophers.db"

class Database:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_db()
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.conn.close()
            self.conn = None

    def _get_connection(self):
        if self.conn:
            return self.conn, False
        return sqlite3.connect(self.db_path), True

    def _init_db(self):
        """Initializes the database schema."""
        # Use a temporary connection for init
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Personalities Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personalities (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                system_prompt TEXT
            )
        ''')

        # Sources Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT NOT NULL,
                filename TEXT NOT NULL,
                content TEXT,
                FOREIGN KEY (personality_id) REFERENCES personalities (id)
            )
        ''')

        # Chunks Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                FOREIGN KEY (source_id) REFERENCES sources (id)
            )
        ''')

        # QA Pairs Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS qa_pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chunk_id INTEGER NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                FOREIGN KEY (chunk_id) REFERENCES chunks (id)
            )
        ''')

        conn.commit()
        conn.close()

    def add_personality(self, p_id: str, name: str, description: str, system_prompt: str):
        conn, should_close = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO personalities (id, name, description, system_prompt)
                VALUES (?, ?, ?, ?)
            ''', (p_id, name, description, system_prompt))
            if should_close:
                conn.commit()
        finally:
            if should_close:
                conn.close()

    def get_personality(self, p_id: str) -> Optional[Dict[str, Any]]:
        conn, should_close = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM personalities WHERE id = ?', (p_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "system_prompt": row[3]
                }
            return None
        finally:
            if should_close:
                conn.close()

    def add_source(self, personality_id: str, filename: str, content: str) -> int:
        conn, should_close = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO sources (personality_id, filename, content)
                VALUES (?, ?, ?)
            ''', (personality_id, filename, content))
            if should_close:
                conn.commit()
            return cursor.lastrowid
        finally:
            if should_close:
                conn.close()

    def add_chunk(self, source_id: int, text: str) -> int:
        conn, should_close = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO chunks (source_id, text)
                VALUES (?, ?)
            ''', (source_id, text))
            if should_close:
                conn.commit()
            return cursor.lastrowid
        finally:
            if should_close:
                conn.close()

    def add_qa_pair(self, chunk_id: int, question: str, answer: str):
        conn, should_close = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO qa_pairs (chunk_id, question, answer)
                VALUES (?, ?, ?)
            ''', (chunk_id, question, answer))
            if should_close:
                conn.commit()
        finally:
            if should_close:
                conn.close()

    def get_qa_pairs(self, personality_id: str) -> List[Dict[str, Any]]:
        """Retrieves all Q&A pairs for a given personality."""
        conn, should_close = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT q.question, q.answer, c.text, s.filename
                FROM qa_pairs q
                JOIN chunks c ON q.chunk_id = c.id
                JOIN sources s ON c.source_id = s.id
                WHERE s.personality_id = ?
            ''', (personality_id,))
            rows = cursor.fetchall()
            return [
                {"question": r[0], "answer": r[1], "context": r[2], "source": r[3]}
                for r in rows
            ]
        finally:
            if should_close:
                conn.close()

    def clear_personality_data(self, personality_id: str):
        """Deletes all sources, chunks, and qa_pairs for a personality."""
        conn, should_close = self._get_connection()
        cursor = conn.cursor()
        try:
            # We need to find source_ids first to delete related chunks and qa_pairs
            cursor.execute('SELECT id FROM sources WHERE personality_id = ?', (personality_id,))
            source_ids = [row[0] for row in cursor.fetchall()]

            if not source_ids:
                return

            cursor.execute(f'SELECT id FROM chunks WHERE source_id IN ({",".join("?"*len(source_ids))})', source_ids)
            chunk_ids = [row[0] for row in cursor.fetchall()]

            if chunk_ids:
                cursor.execute(f'DELETE FROM qa_pairs WHERE chunk_id IN ({",".join("?"*len(chunk_ids))})', chunk_ids)
                cursor.execute(f'DELETE FROM chunks WHERE source_id IN ({",".join("?"*len(source_ids))})', source_ids)

            cursor.execute('DELETE FROM sources WHERE personality_id = ?', (personality_id,))
            if should_close:
                conn.commit()
        finally:
            if should_close:
                conn.close()
