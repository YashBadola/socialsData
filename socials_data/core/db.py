import sqlite3
import json
from pathlib import Path
import logging

DB_PATH = Path("philosophers.db")

class DatabaseManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        if self.conn:
            self.conn.close()

    def initialize_schema(self):
        if not self.conn:
            self.connect()

        cursor = self.conn.cursor()

        # Personalities table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS personalities (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                system_prompt TEXT
            )
        """)

        # Chunks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT,
                text TEXT NOT NULL,
                source TEXT,
                FOREIGN KEY (personality_id) REFERENCES personalities (id)
            )
        """)

        # QA Pairs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS qa_pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chunk_id INTEGER,
                personality_id TEXT,
                instruction TEXT NOT NULL,
                response TEXT NOT NULL,
                source TEXT,
                FOREIGN KEY (chunk_id) REFERENCES chunks (id),
                FOREIGN KEY (personality_id) REFERENCES personalities (id)
            )
        """)

        self.conn.commit()

    def add_personality(self, p_id, name, description, system_prompt):
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO personalities (id, name, description, system_prompt)
                VALUES (?, ?, ?, ?)
            """, (p_id, name, description, system_prompt))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error adding personality {p_id}: {e}")

    def add_chunk(self, personality_id, text, source):
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO chunks (personality_id, text, source)
                VALUES (?, ?, ?)
            """, (personality_id, text, source))
            chunk_id = cursor.lastrowid
            self.conn.commit()
            return chunk_id
        except sqlite3.Error as e:
            logging.error(f"Error adding chunk: {e}")
            return None

    def add_qa_pair(self, instruction, response, chunk_id=None, personality_id=None, source=None):
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO qa_pairs (chunk_id, personality_id, instruction, response, source)
                VALUES (?, ?, ?, ?, ?)
            """, (chunk_id, personality_id, instruction, response, source))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error adding QA pair: {e}")

    def get_personality(self, p_id):
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM personalities WHERE id = ?", (p_id,))
        return cursor.fetchone()

    def get_chunks(self, personality_id):
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM chunks WHERE personality_id = ?", (personality_id,))
        return cursor.fetchall()
