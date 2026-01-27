import sqlite3
import json
from socials_data.db.manager import DatabaseManager

def main():
    manager = DatabaseManager()

    print("Connecting to database...")
    stats = manager.get_stats()
    print("Database Stats:", json.dumps(stats, indent=2))

    print("\n--- Personalities ---")
    conn = manager.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM personalities")
    for row in cursor.fetchall():
        print(f"{row[0]}: {row[1]}")

    print("\n--- Schopenhauer Works ---")
    cursor.execute("SELECT title, url FROM works WHERE personality_id = 'arthur_schopenhauer'")
    for row in cursor.fetchall():
        print(f"Title: {row[0]}, URL: {row[1]}")

    print("\n--- Schopenhauer Segments (First 100 chars) ---")
    segments = manager.get_personality_segments("arthur_schopenhauer", limit=1)
    for seg in segments:
        print(f"{seg[:100]}...")

    conn.close()

if __name__ == "__main__":
    main()
