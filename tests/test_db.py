import sqlite3
import pytest
from pathlib import Path
from socials_data.core.db import init_db, add_personality, get_personality, add_chunk

DB_PATH = Path("test_philosophers.db")

@pytest.fixture
def db_path():
    if DB_PATH.exists():
        DB_PATH.unlink()
    yield DB_PATH
    if DB_PATH.exists():
        DB_PATH.unlink()

def test_init_db(db_path):
    init_db(db_path)
    assert db_path.exists()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='personalities'")
    assert cursor.fetchone() is not None
    conn.close()

def test_add_and_get_personality(db_path):
    init_db(db_path)
    metadata = {
        "id": "test_phil",
        "name": "Test Philosopher",
        "description": "A test description",
        "system_prompt": "You are a test.",
        "sources": [{"title": "Test Book", "type": "book", "url": "http://example.com"}]
    }

    add_personality(db_path, metadata)

    pers = get_personality(db_path, "test_phil")
    assert pers is not None
    assert pers["name"] == "Test Philosopher"

    # Check source
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sources WHERE personality_id = 'test_phil'")
    source = cursor.fetchone()
    assert source is not None
    assert source[2] == "Test Book" # title is 3rd column
    conn.close()

    # Test updating personality (should not duplicate sources)
    add_personality(db_path, metadata)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sources WHERE personality_id = 'test_phil'")
    count = cursor.fetchone()[0]
    assert count == 1
    conn.close()

def test_add_chunk(db_path):
    init_db(db_path)
    metadata = {"id": "test_phil", "name": "Test", "sources": []}
    add_personality(db_path, metadata)

    chunk_id = add_chunk(db_path, "test_phil", "test_source.txt", "Some text")
    assert chunk_id is not None

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT text FROM chunks WHERE id = ?", (chunk_id,))
    row = cursor.fetchone()
    assert row[0] == "Some text"
    conn.close()
