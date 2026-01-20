import sqlite3
import json
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path="philosophers.db"):
        self.db_path = db_path
        self.conn = None
        self.init_db()

    def get_connection(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        return self.conn

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # Create personalities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personalities (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                system_prompt TEXT,
                license TEXT
            )
        ''')

        # Create sources table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT,
                type TEXT,
                title TEXT,
                url TEXT,
                FOREIGN KEY(personality_id) REFERENCES personalities(id)
            )
        ''')

        # Create chunks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT,
                source TEXT,
                text TEXT,
                FOREIGN KEY(personality_id) REFERENCES personalities(id)
            )
        ''')

        conn.commit()

    def add_personality(self, id, name, description, system_prompt, license):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO personalities (id, name, description, system_prompt, license)
            VALUES (?, ?, ?, ?, ?)
        ''', (id, name, description, system_prompt, license))
        conn.commit()

    def add_source(self, personality_id, type, title, url):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sources (personality_id, type, title, url)
            VALUES (?, ?, ?, ?)
        ''', (personality_id, type, title, url))
        conn.commit()

    def add_chunk(self, personality_id, source, text):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO chunks (personality_id, source, text)
            VALUES (?, ?, ?)
        ''', (personality_id, source, text))
        conn.commit()

    def get_personality(self, personality_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM personalities WHERE id = ?', (personality_id,))
        return cursor.fetchone()

    def get_chunks(self, personality_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM chunks WHERE personality_id = ?', (personality_id,))
        return cursor.fetchall()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
