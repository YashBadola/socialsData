import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Optional

class SocialsDatabase:
    def __init__(self, db_path="socials.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        # Create tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS personalities (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                system_prompt TEXT,
                license TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT,
                title TEXT,
                url TEXT,
                type TEXT,
                FOREIGN KEY (personality_id) REFERENCES personalities (id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT,
                source_id INTEGER,
                text TEXT,
                type TEXT, -- 'text' or 'qa'
                meta TEXT, -- JSON blob for extra metadata
                FOREIGN KEY (personality_id) REFERENCES personalities (id),
                FOREIGN KEY (source_id) REFERENCES sources (id)
            )
        ''')
        self.conn.commit()

    def add_personality(self, meta: Dict):
        self.cursor.execute('''
            INSERT OR REPLACE INTO personalities (id, name, description, system_prompt, license)
            VALUES (?, ?, ?, ?, ?)
        ''', (meta['id'], meta['name'], meta.get('description'), meta.get('system_prompt'), meta.get('license')))
        self.conn.commit()

    def add_source(self, personality_id: str, source_meta: Dict) -> int:
        # Check if exists
        title = source_meta.get('title')
        self.cursor.execute('SELECT id FROM sources WHERE personality_id = ? AND title = ?', (personality_id, title))
        row = self.cursor.fetchone()
        if row:
            return row[0]

        self.cursor.execute('''
            INSERT INTO sources (personality_id, title, url, type)
            VALUES (?, ?, ?, ?)
        ''', (personality_id, title, source_meta.get('url'), source_meta.get('type')))
        self.conn.commit()
        return self.cursor.lastrowid

    def add_content(self, personality_id: str, text: str, content_type: str = "text", source_id: Optional[int] = None, meta: Optional[Dict] = None):
        # Check if content exists (naive check by text hash or exact match)
        # For large text, full match is slow, but assuming reasonable chunks.
        self.cursor.execute('SELECT id FROM content WHERE personality_id = ? AND text = ?', (personality_id, text))
        if self.cursor.fetchone():
            return

        self.cursor.execute('''
            INSERT INTO content (personality_id, source_id, text, type, meta)
            VALUES (?, ?, ?, ?, ?)
        ''', (personality_id, source_id, text, content_type, json.dumps(meta) if meta else None))
        self.conn.commit()

    def get_personalities(self):
        self.cursor.execute('SELECT * FROM personalities')
        return self.cursor.fetchall()

    def search_content(self, query: str):
        # Simple LIKE search for now
        self.cursor.execute('SELECT * FROM content WHERE text LIKE ?', (f'%{query}%',))
        return self.cursor.fetchall()

    def close(self):
        if self.conn:
            self.conn.close()

    def sync_from_files(self, personalities_dir: Path):
        """
        Reads from the file system and populates the database.
        """
        self.connect()

        if not personalities_dir.exists():
            print(f"Directory {personalities_dir} does not exist.")
            return

        for personality_path in personalities_dir.iterdir():
            if not personality_path.is_dir():
                continue

            metadata_path = personality_path / "metadata.json"
            if not metadata_path.exists():
                continue

            with open(metadata_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)

            print(f"Syncing {meta['name']}...")
            self.add_personality(meta)

            # Add sources
            source_map = {} # title -> db_id
            if 'sources' in meta:
                for source in meta['sources']:
                    source_id = self.add_source(meta['id'], source)
                    source_map[source.get('title')] = source_id

            # Sync processed data
            processed_data_path = personality_path / "processed" / "data.jsonl"
            if processed_data_path.exists():
                with open(processed_data_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            record = json.loads(line)
                            # Try to link to source
                            # In processor.py, source is the filename (e.g. fear_and_trembling.txt)
                            # In metadata, source has title. We might not match exactly.
                            # For now, we store the filename as source in the DB if not found in map?
                            # Or just ignore linking for now.

                            self.add_content(
                                personality_id=meta['id'],
                                text=record['text'],
                                content_type="text",
                                meta={"source_file": record.get("source")}
                            )
                        except json.JSONDecodeError:
                            continue

            # Sync QA data
            processed_qa_path = personality_path / "processed" / "qa.jsonl"
            if processed_qa_path.exists():
                 with open(processed_qa_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            record = json.loads(line)
                            # QA pair usually has "question" and "answer"
                            # We can store them as one text block or separate?
                            # Let's store as JSON in text or format it.
                            # "Q: ... \nA: ..."
                            text_repr = f"Q: {record.get('question', '')}\nA: {record.get('answer', '')}"
                            self.add_content(
                                personality_id=meta['id'],
                                text=text_repr,
                                content_type="qa",
                                meta={"source_file": record.get("source")}
                            )
                        except json.JSONDecodeError:
                            continue
        print("Sync complete.")
