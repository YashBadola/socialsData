import sqlite3
import json
from pathlib import Path
import logging

DB_PATH = Path(__file__).parent.parent / "data.db"

class DatabaseManager:
    def __init__(self, db_path=None):
        self.db_path = db_path if db_path else DB_PATH
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # Personalities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personalities (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                system_prompt TEXT,
                license TEXT
            )
        ''')

        # Sources table (books, urls) - stored as JSON string in metadata usually, but let's normalize
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

        # Processed Data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS processed_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT,
                source TEXT,
                text TEXT,
                FOREIGN KEY(personality_id) REFERENCES personalities(id)
            )
        ''')

        # QA Pairs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS qa_pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT,
                source TEXT,
                question TEXT,
                answer TEXT,
                FOREIGN KEY(personality_id) REFERENCES personalities(id)
            )
        ''')

        conn.commit()
        conn.close()

    def upsert_personality(self, metadata):
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT OR REPLACE INTO personalities (id, name, description, system_prompt, license)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                metadata['id'],
                metadata.get('name', ''),
                metadata.get('description', ''),
                metadata.get('system_prompt', ''),
                metadata.get('license', 'Unknown')
            ))

            # Clear existing sources and re-insert
            cursor.execute('DELETE FROM sources WHERE personality_id = ?', (metadata['id'],))
            for source in metadata.get('sources', []):
                cursor.execute('''
                    INSERT INTO sources (personality_id, type, title, url)
                    VALUES (?, ?, ?, ?)
                ''', (
                    metadata['id'],
                    source.get('type', ''),
                    source.get('title', ''),
                    source.get('url', '')
                ))

            conn.commit()
        except Exception as e:
            logging.error(f"Error upserting personality {metadata.get('id')}: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()

    def insert_processed_data(self, personality_id, text, source):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO processed_data (personality_id, source, text)
                VALUES (?, ?, ?)
            ''', (personality_id, source, text))
            conn.commit()
        finally:
            conn.close()

    def clear_qa_pairs(self, personality_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM qa_pairs WHERE personality_id = ?', (personality_id,))
            conn.commit()
        finally:
            conn.close()

    def get_processed_data(self, personality_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT text, source FROM processed_data WHERE personality_id = ?', (personality_id,))
            return cursor.fetchall()
        finally:
            conn.close()

    def insert_qa_pair(self, personality_id, source, question, answer):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO qa_pairs (personality_id, source, question, answer)
                VALUES (?, ?, ?, ?)
            ''', (personality_id, source, question, answer))
            conn.commit()
        finally:
            conn.close()

    def clear_processed_data(self, personality_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM processed_data WHERE personality_id = ?', (personality_id,))
            cursor.execute('DELETE FROM qa_pairs WHERE personality_id = ?', (personality_id,))
            conn.commit()
        finally:
            conn.close()
