import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Optional, Any

class DatabaseManager:
    def __init__(self, db_path: str = "socials_data/philosophers.db"):
        self.db_path = db_path
        self._create_tables()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def _create_tables(self):
        """Creates the elaborate schema for the philosopher's dataset."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # 1. Personalities Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS personalities (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                system_prompt TEXT
            )
        """)

        # 2. Works Table (Sources)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS works (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personality_id TEXT NOT NULL,
                title TEXT NOT NULL,
                url TEXT,
                FOREIGN KEY (personality_id) REFERENCES personalities (id)
            )
        """)

        # 3. Segments Table (Text chunks)
        # We add 'chapter_title' and 'sequence_index' for more structure
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS segments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                work_id INTEGER,
                personality_id TEXT NOT NULL,
                content TEXT NOT NULL,
                chapter_title TEXT,
                sequence_index INTEGER,
                FOREIGN KEY (work_id) REFERENCES works (id),
                FOREIGN KEY (personality_id) REFERENCES personalities (id)
            )
        """)

        # 4. QA Pairs Table (Instruction Tuning Data)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS qa_pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                segment_id INTEGER,
                instruction TEXT NOT NULL,
                response TEXT NOT NULL,
                FOREIGN KEY (segment_id) REFERENCES segments (id)
            )
        """)

        conn.commit()
        conn.close()

    def add_personality(self, p_id: str, name: str, description: str, system_prompt: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO personalities (id, name, description, system_prompt)
            VALUES (?, ?, ?, ?)
        """, (p_id, name, description, system_prompt))
        conn.commit()
        conn.close()

    def add_work(self, personality_id: str, title: str, url: str = None) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        # Check if exists
        cursor.execute("SELECT id FROM works WHERE personality_id = ? AND title = ?", (personality_id, title))
        row = cursor.fetchone()
        if row:
            conn.close()
            return row[0]

        cursor.execute("""
            INSERT INTO works (personality_id, title, url)
            VALUES (?, ?, ?)
        """, (personality_id, title, url))
        work_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return work_id

    def add_segment(self, personality_id: str, content: str, work_id: Optional[int] = None, chapter_title: str = None, sequence_index: int = 0) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO segments (personality_id, work_id, content, chapter_title, sequence_index)
            VALUES (?, ?, ?, ?, ?)
        """, (personality_id, work_id, content, chapter_title, sequence_index))
        segment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return segment_id

    def add_qa_pair(self, segment_id: int, instruction: str, response: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO qa_pairs (segment_id, instruction, response)
            VALUES (?, ?, ?)
        """, (segment_id, instruction, response))
        conn.commit()
        conn.close()

    def get_stats(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        stats = {}
        cursor.execute("SELECT COUNT(*) FROM personalities")
        stats["personalities"] = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM works")
        stats["works"] = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM segments")
        stats["segments"] = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM qa_pairs")
        stats["qa_pairs"] = cursor.fetchone()[0]
        conn.close()
        return stats

    def get_personality_segments(self, personality_id: str, limit: int = 5):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM segments WHERE personality_id = ? LIMIT ?", (personality_id, limit))
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]
