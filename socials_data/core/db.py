import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "socials.db"

class SocialsDatabase:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

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

        # Sources table
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

        # Content chunks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT,
                text TEXT,
                source_file TEXT,
                FOREIGN KEY(personality_id) REFERENCES personalities(id)
            )
        ''')

        conn.commit()
        conn.close()

    def upsert_personality(self, metadata):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        p_id = metadata['id']

        cursor.execute('''
            INSERT INTO personalities (id, name, description, system_prompt, license)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name=excluded.name,
                description=excluded.description,
                system_prompt=excluded.system_prompt,
                license=excluded.license
        ''', (
            p_id,
            metadata.get('name', ''),
            metadata.get('description', ''),
            metadata.get('system_prompt', ''),
            metadata.get('license', '')
        ))

        # Clear existing sources and re-insert
        cursor.execute('DELETE FROM sources WHERE personality_id = ?', (p_id,))
        for source in metadata.get('sources', []):
            cursor.execute('''
                INSERT INTO sources (personality_id, type, title, url)
                VALUES (?, ?, ?, ?)
            ''', (p_id, source.get('type', ''), source.get('title', ''), source.get('url', '')))

        conn.commit()
        conn.close()

    def index_chunks(self, personality_id, chunks):
        """
        chunks: list of dicts with 'text' and 'source' keys
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # We might want to clear existing chunks for this personality to avoid duplicates on re-index
        cursor.execute('DELETE FROM content_chunks WHERE personality_id = ?', (personality_id,))

        for chunk in chunks:
            cursor.execute('''
                INSERT INTO content_chunks (personality_id, text, source_file)
                VALUES (?, ?, ?)
            ''', (personality_id, chunk.get('text', ''), chunk.get('source', '')))

        conn.commit()
        conn.close()

    def get_personality(self, personality_id):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM personalities WHERE id = ?', (personality_id,))
        row = cursor.fetchone()

        if not row:
            conn.close()
            return None

        personality = dict(row)

        cursor.execute('SELECT type, title, url FROM sources WHERE personality_id = ?', (personality_id,))
        personality['sources'] = [dict(r) for r in cursor.fetchall()]

        conn.close()
        return personality

    def search_content(self, query):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Simple LIKE search
        cursor.execute('''
            SELECT p.name, c.text, c.source_file
            FROM content_chunks c
            JOIN personalities p ON c.personality_id = p.id
            WHERE c.text LIKE ?
        ''', (f'%{query}%',))

        results = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return results
