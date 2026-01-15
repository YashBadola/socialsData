import sqlite3
import json
import argparse
from pathlib import Path

def export_to_sqlite(personality_id, db_path=None):
    # Adjust path if running from root
    base_dir = Path("socials_data/personalities")
    personality_dir = base_dir / personality_id
    processed_dir = personality_dir / "processed"
    data_file = processed_dir / "data.jsonl"

    if not data_file.exists():
        # Try absolute path or relative to script if needed, but assuming running from root
        print(f"Error: {data_file} not found.")
        return

    if db_path is None:
        db_path = processed_dir / "database.sqlite"

    print(f"Exporting {personality_id} to {db_path}...")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            source TEXT
        )
    ''')

    # Insert data
    with open(data_file, 'r') as f:
        for line in f:
            entry = json.loads(line)
            text = entry.get('text', '')
            source = entry.get('source', 'unknown')
            cursor.execute('INSERT INTO content (text, source) VALUES (?, ?)', (text, source))

    conn.commit()
    conn.close()
    print("Export complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export processed JSONL data to SQLite.")
    parser.add_argument("personality_id", help="The ID of the personality (e.g., michel_de_montaigne)")
    parser.add_argument("--output", help="Optional output path for the SQLite database")

    args = parser.parse_args()
    export_to_sqlite(args.personality_id, args.output)
