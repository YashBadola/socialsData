from socials_data.core.db import SocialsDatabase
from pathlib import Path
import shutil
import os

def test_sync():
    # Use a temporary DB
    db_path = "test_socials.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    db = SocialsDatabase(db_path=db_path)

    # Sync
    personalities_dir = Path("socials_data/personalities")
    db.sync_from_files(personalities_dir)

    # Run sync again to test idempotency
    print("Running sync again...")
    db.sync_from_files(personalities_dir)

    # Query
    db.connect()

    # Check Kierkegaard
    print("Checking for Søren Kierkegaard...")
    db.cursor.execute("SELECT id, name FROM personalities WHERE id='soren_kierkegaard'")
    res = db.cursor.fetchone()
    if res:
        print(f"Found: {res}")
    else:
        print("Not Found!")

    # Check Content
    print("Checking content for Søren Kierkegaard...")
    db.cursor.execute("SELECT count(*) FROM content WHERE personality_id='soren_kierkegaard'")
    count = db.cursor.fetchone()[0]
    print(f"Content count: {count}")

    assert count == 1, f"Expected 1 content item, found {count}. Idempotency failed?"
    print("Idempotency check passed.")

    # Check specific text content
    print("Checking specific text content...")
    db.cursor.execute("SELECT text FROM content WHERE personality_id='soren_kierkegaard' LIMIT 1")
    text = db.cursor.fetchone()[0]
    print(f"Sample text: {text[:100]}...")

    # Verify we can find other personalities too (existing ones)
    print("Checking for Friedrich Nietzsche...")
    db.cursor.execute("SELECT id, name FROM personalities WHERE id='friedrich_nietzsche'")
    res = db.cursor.fetchone()
    assert res is not None, "Nietzsche Not Found! (Maybe data not processed?)"
    print(f"Found: {res}")

    db.close()

    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)

if __name__ == "__main__":
    test_sync()
