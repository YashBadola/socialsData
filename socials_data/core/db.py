import sqlite3
import json
from pathlib import Path

DB_PATH = Path("philosophers.db")

def init_db(db_path=DB_PATH):
    """Initializes the SQLite database with the required schema."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Personalities table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS personalities (
        id TEXT PRIMARY KEY,
        name TEXT,
        description TEXT,
        system_prompt TEXT,
        license TEXT
    )
    """)

    # Sources table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        personality_id TEXT,
        title TEXT,
        type TEXT,
        url TEXT,
        FOREIGN KEY(personality_id) REFERENCES personalities(id)
    )
    """)

    # Chunks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        personality_id TEXT,
        source_filename TEXT,
        text TEXT,
        embedding BLOB,
        FOREIGN KEY(personality_id) REFERENCES personalities(id)
    )
    """)

    # QA Pairs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS qa_pairs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        personality_id TEXT,
        chunk_id INTEGER,
        instruction TEXT,
        response TEXT,
        source_filename TEXT,
        FOREIGN KEY(personality_id) REFERENCES personalities(id),
        FOREIGN KEY(chunk_id) REFERENCES chunks(id)
    )
    """)

    conn.commit()
    conn.close()

def add_personality(db_path, metadata):
    """Adds or updates a personality."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO personalities (id, name, description, system_prompt, license)
    VALUES (?, ?, ?, ?, ?)
    """, (
        metadata["id"],
        metadata["name"],
        metadata.get("description", ""),
        metadata.get("system_prompt", ""),
        metadata.get("license", "Unknown")
    ))

    # Add sources
    # First, remove existing sources to avoid duplicates
    cursor.execute("DELETE FROM sources WHERE personality_id = ?", (metadata["id"],))

    if "sources" in metadata:
        for source in metadata["sources"]:
            cursor.execute("""
            INSERT INTO sources (personality_id, title, type, url)
            VALUES (?, ?, ?, ?)
            """, (
                metadata["id"],
                source.get("title", ""),
                source.get("type", ""),
                source.get("url", "")
            ))

    conn.commit()
    conn.close()

def add_chunk(db_path, personality_id, source_filename, text):
    """Adds a text chunk."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO chunks (personality_id, source_filename, text)
    VALUES (?, ?, ?)
    """, (personality_id, source_filename, text))

    chunk_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return chunk_id

def add_qa_pair(db_path, personality_id, chunk_id, instruction, response, source_filename):
    """Adds a QA pair."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO qa_pairs (personality_id, chunk_id, instruction, response, source_filename)
    VALUES (?, ?, ?, ?, ?)
    """, (personality_id, chunk_id, instruction, response, source_filename))

    conn.commit()
    conn.close()

def get_personality(db_path, personality_id):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM personalities WHERE id = ?", (personality_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None
