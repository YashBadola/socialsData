import sqlite3
import json
from pathlib import Path

class SocialsDatabase:
    def __init__(self, db_path="socials.db"):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def init_db(self):
        self.connect()
        cursor = self.conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS personalities (
            id TEXT PRIMARY KEY,
            name TEXT,
            description TEXT,
            system_prompt TEXT,
            metadata JSON
        )
        ''')

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

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            personality_id TEXT,
            source TEXT,
            text TEXT,
            type TEXT DEFAULT 'text', -- 'text' or 'qa'
            FOREIGN KEY(personality_id) REFERENCES personalities(id)
        )
        ''')

        # FTS table for full text search
        try:
            cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS content_fts USING fts5(
                personality_id,
                source,
                text,
                content='content',
                content_rowid='id'
            )
            ''')

            # Triggers to keep FTS updated
            cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS content_ai AFTER INSERT ON content BEGIN
              INSERT INTO content_fts(rowid, personality_id, source, text) VALUES (new.id, new.personality_id, new.source, new.text);
            END;
            ''')

            cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS content_ad AFTER DELETE ON content BEGIN
              INSERT INTO content_fts(content_fts, rowid, personality_id, source, text) VALUES('delete', old.id, old.personality_id, old.source, old.text);
            END;
            ''')

            cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS content_au AFTER UPDATE ON content BEGIN
              INSERT INTO content_fts(content_fts, rowid, personality_id, source, text) VALUES('delete', old.id, old.personality_id, old.source, old.text);
              INSERT INTO content_fts(rowid, personality_id, source, text) VALUES (new.id, new.personality_id, new.source, new.text);
            END;
            ''')
        except sqlite3.OperationalError:
            print("Warning: FTS5 not supported. Full-text search will not be available.")

        self.conn.commit()

    def ingest_personality(self, personality_id, base_dir):
        """
        Ingests a personality into the database from the file system.
        """
        base_dir = Path(base_dir)
        p_dir = base_dir / personality_id

        if not p_dir.exists():
            raise FileNotFoundError(f"Personality {personality_id} not found at {base_dir}")

        self.connect()
        cursor = self.conn.cursor()

        # 1. Read Metadata
        metadata_path = p_dir / "metadata.json"
        real_id = personality_id
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                meta = json.load(f)

            real_id = meta.get('id', personality_id)

            cursor.execute('''
            INSERT OR REPLACE INTO personalities (id, name, description, system_prompt, metadata)
            VALUES (?, ?, ?, ?, ?)
            ''', (
                real_id,
                meta.get('name'),
                meta.get('description'),
                meta.get('system_prompt'),
                json.dumps(meta)
            ))

            # Sources
            cursor.execute('DELETE FROM sources WHERE personality_id = ?', (real_id,))
            for source in meta.get('sources', []):
                cursor.execute('''
                INSERT INTO sources (personality_id, title, url, type)
                VALUES (?, ?, ?, ?)
                ''', (real_id, source.get('title'), source.get('url'), source.get('type')))

        # 2. Read Processed Data
        data_path = p_dir / "processed" / "data.jsonl"
        if data_path.exists():
            # Clear existing content for this personality (simple approach)
            # Note: This is inefficient for large datasets but fine for this scope
            cursor.execute('DELETE FROM content WHERE personality_id = ?', (real_id,))

            with open(data_path, 'r') as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        cursor.execute('''
                        INSERT INTO content (personality_id, source, text, type)
                        VALUES (?, ?, ?, 'text')
                        ''', (real_id, record.get('source'), record.get('text')))
                    except json.JSONDecodeError:
                        continue

        # 3. Read QA Data (optional)
        qa_path = p_dir / "processed" / "qa.jsonl"
        if qa_path.exists():
            with open(qa_path, 'r') as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        # We store QA as text, maybe formatted
                        text = f"Q: {record.get('question')}\nA: {record.get('answer')}"
                        cursor.execute('''
                        INSERT INTO content (personality_id, source, text, type)
                        VALUES (?, ?, ?, 'qa')
                        ''', (real_id, record.get('source'), text))
                    except json.JSONDecodeError:
                        continue

        self.conn.commit()

    def search(self, query):
        self.connect()
        cursor = self.conn.cursor()

        try:
            # Use FTS
            cursor.execute('''
            SELECT personality_id, source, text
            FROM content_fts
            WHERE content_fts MATCH ?
            ORDER BY rank
            LIMIT 20
            ''', (query,))
        except sqlite3.OperationalError:
            # Fallback to LIKE
            cursor.execute('''
            SELECT personality_id, source, text
            FROM content
            WHERE text LIKE ?
            LIMIT 20
            ''', (f"%{query}%",))

        return [dict(row) for row in cursor.fetchall()]
