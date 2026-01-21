import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "philosophers.db"

class DatabaseManager:
    def __init__(self, db_path=None):
        self.db_path = db_path if db_path else DB_PATH
        self.conn = None
        self._initialize_db()

    def _get_connection(self):
        if not self.conn:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        return self.conn

    def _initialize_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()

        # Personalities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personalities (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                system_prompt TEXT
            )
        ''')

        # Works/Sources table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS works (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT NOT NULL,
                title TEXT NOT NULL,
                type TEXT,
                url TEXT,
                FOREIGN KEY (personality_id) REFERENCES personalities (id)
            )
        ''')

        # Content/Excerpts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS excerpts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                work_id INTEGER,
                text TEXT NOT NULL,
                chapter TEXT,
                page TEXT,
                source_filename TEXT,
                FOREIGN KEY (work_id) REFERENCES works (id)
            )
        ''')

        conn.commit()

    def add_personality(self, p_id, name, description, system_prompt):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO personalities (id, name, description, system_prompt)
            VALUES (?, ?, ?, ?)
        ''', (p_id, name, description, system_prompt))
        conn.commit()

    def add_work(self, personality_id, title, work_type, url):
        conn = self._get_connection()
        cursor = conn.cursor()

        # Check if exists
        cursor.execute('SELECT id FROM works WHERE personality_id = ? AND title = ?', (personality_id, title))
        row = cursor.fetchone()
        if row:
            return row['id']

        cursor.execute('''
            INSERT INTO works (personality_id, title, type, url)
            VALUES (?, ?, ?, ?)
        ''', (personality_id, title, work_type, url))
        conn.commit()
        return cursor.lastrowid

    def add_excerpt(self, work_id, text, chapter=None, page=None, source_filename=None):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO excerpts (work_id, text, chapter, page, source_filename)
            VALUES (?, ?, ?, ?, ?)
        ''', (work_id, text, chapter, page, source_filename))
        conn.commit()
        return cursor.lastrowid

    def get_personality(self, p_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM personalities WHERE id = ?', (p_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_excerpts_by_personality(self, p_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT e.text, w.title, p.name
            FROM excerpts e
            JOIN works w ON e.work_id = w.id
            JOIN personalities p ON w.personality_id = p.id
            WHERE p.id = ?
        ''', (p_id,))
        return [dict(row) for row in cursor.fetchall()]

    def clear_personality_data(self, p_id):
        """Removes all data associated with a personality ID to allow re-population."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Get work IDs to delete excerpts
        cursor.execute('SELECT id FROM works WHERE personality_id = ?', (p_id,))
        work_ids = [row['id'] for row in cursor.fetchall()]

        if work_ids:
            # Delete excerpts for these works
            placeholders = ','.join('?' * len(work_ids))
            cursor.execute(f'DELETE FROM excerpts WHERE work_id IN ({placeholders})', work_ids)

            # Delete works
            cursor.execute('DELETE FROM works WHERE personality_id = ?', (p_id,))

        # Delete personality entry
        cursor.execute('DELETE FROM personalities WHERE id = ?', (p_id,))

        conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
