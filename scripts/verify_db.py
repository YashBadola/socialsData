import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "socials_data" / "philosophers.db"

def verify():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Query for Arthur Schopenhauer
    cursor.execute("SELECT name FROM personalities WHERE id='arthur_schopenhauer'")
    name = cursor.fetchone()

    if not name:
        print("FAIL: Arthur Schopenhauer not found in personalities table.")
        sys.exit(1)

    print(f"SUCCESS: Found personality: {name[0]}")

    cursor.execute("SELECT COUNT(*) FROM content WHERE personality_id='arthur_schopenhauer'")
    count = cursor.fetchone()[0]

    print(f"SUCCESS: Found {count} content entries for Arthur Schopenhauer.")

    if count == 0:
         print("FAIL: No content entries found.")
         sys.exit(1)

    # Fetch one entry
    cursor.execute("SELECT text FROM content WHERE personality_id='arthur_schopenhauer' LIMIT 1")
    text = cursor.fetchone()[0]
    print(f"Sample text: {text[:100]}...")

    conn.close()

if __name__ == "__main__":
    verify()
