import sqlite3
from pathlib import Path
import json

class DatabaseManager:
    def __init__(self, db_path="socials_data.db"):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _init_db(self):
        conn = self._get_conn()
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

        # Works/Sources Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS works (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT,
                title TEXT,
                type TEXT,
                url TEXT,
                FOREIGN KEY (personality_id) REFERENCES personalities(id)
            )
        ''')

        # Content/Excerpts Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS excerpts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                work_id INTEGER,
                personality_id TEXT,
                text TEXT NOT NULL,
                chapter TEXT,
                page TEXT,
                source_file TEXT,
                FOREIGN KEY (work_id) REFERENCES works(id),
                FOREIGN KEY (personality_id) REFERENCES personalities(id)
            )
        ''')

        conn.commit()
        conn.close()

    def add_personality(self, id, name, description, system_prompt):
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO personalities (id, name, description, system_prompt)
                VALUES (?, ?, ?, ?)
            ''', (id, name, description, system_prompt))
            conn.commit()
        finally:
            conn.close()

    def add_work(self, personality_id, title, type="unknown", url=None):
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO works (personality_id, title, type, url)
                VALUES (?, ?, ?, ?)
            ''', (personality_id, title, type, url))
            work_id = cursor.lastrowid
            conn.commit()
            return work_id
        finally:
            conn.close()

    def add_excerpt(self, personality_id, text, work_id=None, source_file=None):
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO excerpts (personality_id, work_id, text, source_file)
                VALUES (?, ?, ?, ?)
            ''', (personality_id, work_id, text, source_file))
            conn.commit()
        finally:
            conn.close()

    def get_personality(self, personality_id):
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM personalities WHERE id = ?', (personality_id,))
            return cursor.fetchone()
        finally:
            conn.close()

    def get_excerpts(self, personality_id):
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT text FROM excerpts WHERE personality_id = ?', (personality_id,))
            return [row[0] for row in cursor.fetchall()]
        finally:
            conn.close()
