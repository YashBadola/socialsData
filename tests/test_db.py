import pytest
import os
from pathlib import Path
from socials_data.core.db import SocialsDatabase

@pytest.fixture
def temp_db(tmp_path):
    db_path = tmp_path / "test_socials.db"
    return SocialsDatabase(db_path)

def test_init_db(temp_db):
    assert temp_db.db_path.exists()

def test_upsert_get_personality(temp_db):
    metadata = {
        "id": "test_philosopher",
        "name": "Test Philosopher",
        "description": "A test description.",
        "system_prompt": "You are a test.",
        "sources": [
            {"type": "book", "title": "Test Book", "url": "http://example.com"}
        ],
        "license": "MIT"
    }

    temp_db.upsert_personality(metadata)

    p = temp_db.get_personality("test_philosopher")
    assert p is not None
    assert p["name"] == "Test Philosopher"
    assert len(p["sources"]) == 1
    assert p["sources"][0]["title"] == "Test Book"

def test_index_search_content(temp_db):
    # Setup personality
    temp_db.upsert_personality({"id": "p1", "name": "P1"})

    chunks = [
        {"text": "The quick brown fox.", "source": "file1.txt"},
        {"text": "Jumps over the lazy dog.", "source": "file2.txt"}
    ]

    temp_db.index_chunks("p1", chunks)

    # Search
    results = temp_db.search_content("fox")
    assert len(results) == 1
    assert results[0]["text"] == "The quick brown fox."
    assert results[0]["name"] == "P1"

    results = temp_db.search_content("dog")
    assert len(results) == 1

    results = temp_db.search_content("cat")
    assert len(results) == 0
