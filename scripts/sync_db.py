from socials_data.core.db import SocialsDatabase
from pathlib import Path

def main():
    db = SocialsDatabase("socials.db")
    # Initialize DB (creates tables)
    db.connect()

    personalities_dir = Path("socials_data/personalities")
    print(f"Syncing from {personalities_dir}...")
    db.sync_from_files(personalities_dir)

    print("Verifying Søren Kierkegaard...")
    # Verify
    cursor = db.conn.cursor()
    cursor.execute("SELECT * FROM personalities WHERE id = 'soren_kierkegaard'")
    p = cursor.fetchone()
    if p:
        print(f"Found personality: {p[1]}")
    else:
        print("Søren Kierkegaard NOT found!")

    cursor.execute("SELECT count(*) FROM content WHERE personality_id = 'soren_kierkegaard'")
    count = cursor.fetchone()[0]
    print(f"Found {count} content records for Søren Kierkegaard.")

    if count > 0:
        cursor.execute("SELECT text FROM content WHERE personality_id = 'soren_kierkegaard' LIMIT 1")
        text = cursor.fetchone()[0]
        print(f"Sample text: {text[:100]}...")

    db.close()

if __name__ == "__main__":
    main()
