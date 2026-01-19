import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data.db"

class SocialsDatabase:
    def __init__(self, db_path=None):
        self.db_path = db_path if db_path else DB_PATH
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        if self.conn:
            self.conn.close()

    def init_db(self):
        """Initialize the database schema."""
        if not self.conn:
            self.connect()

        cursor = self.conn.cursor()

        # Personalities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personalities (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                system_prompt TEXT,
                metadata TEXT
            )
        ''')

        # Sources table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT,
                title TEXT,
                url TEXT,
                type TEXT,
                FOREIGN KEY(personality_id) REFERENCES personalities(id)
            )
        ''')

        # Content table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT,
                source_id INTEGER,
                text TEXT,
                type TEXT,
                meta TEXT,
                FOREIGN KEY(personality_id) REFERENCES personalities(id),
                FOREIGN KEY(source_id) REFERENCES sources(id)
            )
        ''')

        # Enable FTS5 for full-text search on content
        cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS content_fts USING fts5(text, content='content', content_rowid='id')
        ''')

        # Triggers to keep FTS index up to date
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS content_ai AFTER INSERT ON content BEGIN
              INSERT INTO content_fts(rowid, text) VALUES (new.id, new.text);
            END;
        ''')
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS content_ad AFTER DELETE ON content BEGIN
              INSERT INTO content_fts(content_fts, rowid, text) VALUES('delete', old.id, old.text);
            END;
        ''')
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS content_au AFTER UPDATE ON content BEGIN
              INSERT INTO content_fts(content_fts, rowid, text) VALUES('delete', old.id, old.text);
              INSERT INTO content_fts(rowid, text) VALUES (new.id, new.text);
            END;
        ''')

        self.conn.commit()

    def upsert_personality(self, p_id, name, description, system_prompt, metadata=None):
        if not self.conn:
            self.connect()

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO personalities (id, name, description, system_prompt, metadata)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name=excluded.name,
                description=excluded.description,
                system_prompt=excluded.system_prompt,
                metadata=excluded.metadata
        ''', (p_id, name, description, system_prompt, json.dumps(metadata) if metadata else None))
        self.conn.commit()

    def add_source(self, personality_id, title, url, s_type):
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor()

        # Check if exists
        cursor.execute('''
            SELECT id FROM sources WHERE personality_id = ? AND title = ?
        ''', (personality_id, title))
        row = cursor.fetchone()
        if row:
            return row['id']

        cursor.execute('''
            INSERT INTO sources (personality_id, title, url, type)
            VALUES (?, ?, ?, ?)
        ''', (personality_id, title, url, s_type))
        self.conn.commit()
        return cursor.lastrowid

    def add_content(self, personality_id, text, c_type, source_id=None, meta=None):
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor()

        cursor.execute('''
            INSERT INTO content (personality_id, source_id, text, type, meta)
            VALUES (?, ?, ?, ?, ?)
        ''', (personality_id, source_id, text, c_type, json.dumps(meta) if meta else None))
        self.conn.commit()

    def clear_personality_content(self, personality_id):
        """Clears content for a personality before re-syncing."""
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM content WHERE personality_id = ?", (personality_id,))
        # Sources are usually stable, but we could clear them too if we want a full resync.
        # For now, let's keep sources but maybe update them.
        self.conn.commit()

    def search(self, query, limit=10):
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT c.text, p.name, c.type
            FROM content_fts
            JOIN content c ON c.id = content_fts.rowid
            JOIN personalities p ON c.personality_id = p.id
            WHERE content_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        ''', (query, limit))
        return cursor.fetchall()
