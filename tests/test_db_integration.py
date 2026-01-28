import pytest
import sqlite3
from pathlib import Path
from socials_data.core.db import DatabaseManager

@pytest.fixture
def test_db(tmp_path):
    """Creates a temporary database for testing."""
    db_path = tmp_path / "test_socials.db"
    db = DatabaseManager(db_path)
    db.init_db()
    return db

def test_db_tables_created(test_db):
    """Verifies that tables are created."""
    conn = test_db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    assert "personalities" in tables
    assert "content" in tables
    assert "qa_pairs" in tables
    conn.close()

def test_sync_personality_and_query(test_db, tmp_path):
    """Verifies syncing data and querying it."""
    # Create a dummy personality structure
    p_dir = tmp_path / "dummy_philosopher"
    p_dir.mkdir()
    (p_dir / "raw").mkdir()
    processed_dir = (p_dir / "processed")
    processed_dir.mkdir()

    # Metadata
    metadata = {
        "name": "Dummy Philosopher",
        "id": "dummy_p",
        "description": "A test philosopher.",
        "system_prompt": "You are a test."
    }
    import json
    with open(p_dir / "metadata.json", "w") as f:
        json.dump(metadata, f)

    # Data
    with open(processed_dir / "data.jsonl", "w") as f:
        f.write(json.dumps({"text": "I think therefore I test.", "source": "test.txt"}) + "\n")

    # Sync
    test_db.sync_personality("dummy_p", p_dir)

    # Query Personality
    cols, res = test_db.query("SELECT name FROM personalities WHERE id='dummy_p'")
    assert res[0][0] == "Dummy Philosopher"

    # Query Content
    cols, res = test_db.query("SELECT text FROM content WHERE personality_id='dummy_p'")
    assert res[0][0] == "I think therefore I test."
