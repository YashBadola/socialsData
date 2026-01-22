import sqlite3
from pathlib import Path
from typing import List, Dict, Optional, Any

class DatabaseManager:
    def __init__(self, db_path: str = "socials_data/philosophers.db"):
        self.db_path = Path(db_path)
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Initialize the database with the schema."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personalities (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                system_prompt TEXT,
                license TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT NOT NULL,
                title TEXT,
                url TEXT,
                type TEXT,
                FOREIGN KEY (personality_id) REFERENCES personalities (id)
            )
        ''')

        conn.commit()
        conn.close()

    def add_personality(self, personality_data: Dict[str, Any]):
        """Add or update a personality and their sources."""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Insert or update personality
            cursor.execute('''
                INSERT OR REPLACE INTO personalities (id, name, description, system_prompt, license)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                personality_data['id'],
                personality_data['name'],
                personality_data.get('description', ''),
                personality_data.get('system_prompt', ''),
                personality_data.get('license', 'Unknown')
            ))

            # Delete existing sources for this personality (to replace them)
            cursor.execute('DELETE FROM sources WHERE personality_id = ?', (personality_data['id'],))

            # Insert sources
            for source in personality_data.get('sources', []):
                cursor.execute('''
                    INSERT INTO sources (personality_id, title, url, type)
                    VALUES (?, ?, ?, ?)
                ''', (
                    personality_data['id'],
                    source.get('title', ''),
                    source.get('url', ''),
                    source.get('type', '')
                ))

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def get_personality(self, personality_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a personality and their sources by ID."""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM personalities WHERE id = ?', (personality_id,))
        row = cursor.fetchone()

        if not row:
            conn.close()
            return None

        personality = dict(row)

        cursor.execute('SELECT title, url, type FROM sources WHERE personality_id = ?', (personality_id,))
        sources_rows = cursor.fetchall()
        personality['sources'] = [dict(s) for s in sources_rows]

        conn.close()
        return personality

    def list_personalities(self) -> List[Dict[str, Any]]:
        """List all personalities."""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM personalities')
        rows = cursor.fetchall()

        personalities = []
        for row in rows:
            p = dict(row)
            # Fetch sources for each (could be optimized with a join, but this is simple)
            cursor.execute('SELECT title, url, type FROM sources WHERE personality_id = ?', (p['id'],))
            sources_rows = cursor.fetchall()
            p['sources'] = [dict(s) for s in sources_rows]
            personalities.append(p)

        conn.close()
        return personalities
