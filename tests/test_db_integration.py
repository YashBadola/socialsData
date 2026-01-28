import os
import sqlite3
import pytest
from socials_data.core.db import DatabaseManager
from socials_data.core.manager import PersonalityManager
from socials_data.core.processor import TextDataProcessor
from pathlib import Path

# Use a temporary database for testing
TEST_DB = "test_socials.db"

@pytest.fixture
def db_manager():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    manager = DatabaseManager(db_path=TEST_DB)
    manager.init_db()
    yield manager
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_database_init(db_manager):
    """Test that tables are created correctly."""
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    assert "personalities" in tables
    assert "content" in tables
    assert "qa_pairs" in tables
    conn.close()

def test_aristotle_sync(db_manager):
    """Test syncing Aristotle data to the database."""
    # Ensure Aristotle is processed (we need the data.jsonl file)
    # We will assume the file structure exists from Step 1, but we need to run processor
    pm = PersonalityManager()
    # Check if aristotle exists
    try:
        pm.get_metadata("aristotle")
    except FileNotFoundError:
        pytest.fail("Aristotle personality not found. Run Step 1 first.")

    # Process it
    processor = TextDataProcessor()
    personality_dir = pm.base_dir / "aristotle"
    processor.process(personality_dir, skip_qa=True)

    # Sync to DB
    db_manager.sync_personality("aristotle", personality_dir)

    # Verify data in DB
    columns, rows = db_manager.query("SELECT * FROM personalities WHERE id='aristotle'")
    assert len(rows) == 1
    assert rows[0][1] == "Aristotle"

    columns, rows = db_manager.query("SELECT * FROM content WHERE personality_id='aristotle'")
    assert len(rows) >= 1
    # Check content contains some text from the raw file
    assert "state" in rows[0][2] or "community" in rows[0][2]
