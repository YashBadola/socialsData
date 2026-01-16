import pytest
from socials_data.core.database import SocialsDatabase
import os
import json

@pytest.fixture
def db():
    db_path = "test_socials.db"
    db = SocialsDatabase(db_path)
    db.init_db()
    yield db
    db.close()
    if os.path.exists(db_path):
        os.remove(db_path)

def test_database_init(db):
    db.connect()
    cursor = db.conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='personalities'")
    assert cursor.fetchone() is not None
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='content'")
    assert cursor.fetchone() is not None

def test_sync_and_query(db, tmp_path):
    # Setup dummy personality
    personality_dir = tmp_path / "test_personality"
    personality_dir.mkdir()
    (personality_dir / "raw").mkdir()
    (personality_dir / "processed").mkdir()

    metadata = {
        "name": "Test Person",
        "description": "A test personality."
    }
    with open(personality_dir / "metadata.json", "w") as f:
        json.dump(metadata, f)

    data = {"text": "This is a sample text for testing.", "source": "test.txt"}
    with open(personality_dir / "processed" / "data.jsonl", "w") as f:
        f.write(json.dumps(data) + "\n")

    db.sync_personality("test_personality", str(personality_dir))

    results = db.query("sample")
    assert len(results) == 1
    assert results[0]['name'] == "Test Person"
    assert results[0]['text'] == "This is a sample text for testing."
