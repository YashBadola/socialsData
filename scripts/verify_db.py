import sqlite3
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

def verify():
    # Robust path resolution
    repo_root = Path(__file__).parent.parent
    db_path = repo_root / "socials_data" / "philosophers.db"

    if not db_path.exists():
        print(f"Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("--- Personalities ---")
    cursor.execute("SELECT id, name FROM personalities")
    for row in cursor.fetchall():
        print(row)

    print("\n--- Kierkegaard Sources ---")
    cursor.execute("SELECT title, url FROM sources WHERE personality_id = 'soren_kierkegaard'")
    for row in cursor.fetchall():
        print(row)

    conn.close()

if __name__ == "__main__":
    verify()
