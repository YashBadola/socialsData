import sqlite3
import json
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
PERSONALITIES_DIR = BASE_DIR / "socials_data" / "personalities"
DB_PATH = BASE_DIR / "socials_data" / "philosophers.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
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

    # Create content table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS content (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        personality_id TEXT,
        text TEXT,
        source TEXT,
        type TEXT,
        FOREIGN KEY(personality_id) REFERENCES personalities(id)
    )
    ''')

    # Create sources table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        personality_id TEXT,
        title TEXT,
        type TEXT,
        url TEXT,
        FOREIGN KEY(personality_id) REFERENCES personalities(id)
    )
    ''')

    conn.commit()
    return conn

def populate_db(conn):
    cursor = conn.cursor()

    # Iterate over personalities
    for personality_dir in PERSONALITIES_DIR.iterdir():
        if not personality_dir.is_dir():
            continue

        metadata_path = personality_dir / "metadata.json"
        if not metadata_path.exists():
            continue

        # Read metadata
        try:
            with open(metadata_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)

            p_id = metadata.get("id")
            name = metadata.get("name")
            desc = metadata.get("description")
            sys_prompt = metadata.get("system_prompt")
            license_ = metadata.get("license")
            sources = metadata.get("sources", [])

            cursor.execute('''
            INSERT INTO personalities (id, name, description, system_prompt, license)
            VALUES (?, ?, ?, ?, ?)
            ''', (p_id, name, desc, sys_prompt, license_))

            # Insert sources
            for src in sources:
                cursor.execute('''
                INSERT INTO sources (personality_id, title, type, url)
                VALUES (?, ?, ?, ?)
                ''', (p_id, src.get("title"), src.get("type"), src.get("url")))

            print(f"Inserted personality: {name}")

            # Read processed data
            data_path = personality_dir / "processed" / "data.jsonl"
            if data_path.exists():
                with open(data_path, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            record = json.loads(line)
                            text = record.get("text")
                            source = record.get("source")

                            cursor.execute('''
                            INSERT INTO content (personality_id, text, source, type)
                            VALUES (?, ?, ?, 'text')
                            ''', (p_id, text, source))
                        except json.JSONDecodeError:
                            continue
                print(f"  Inserted content for {name}")

        except Exception as e:
            print(f"Error processing {personality_dir.name}: {e}")

    conn.commit()

def main():
    if DB_PATH.exists():
        print(f"Removing existing database at {DB_PATH}...")
        os.remove(DB_PATH)

    print(f"Building database at {DB_PATH}...")
    conn = init_db()
    populate_db(conn)
    conn.close()
    print("Database build complete.")

if __name__ == "__main__":
    main()
