import pytest
import os
from socials_data.core.db import DatabaseManager

@pytest.fixture
def db(tmp_path):
    # Use a temporary file for the database
    db_path = tmp_path / "test.db"
    manager = DatabaseManager(db_path=db_path)
    yield manager
    manager.close()

def test_add_personality(db):
    db.add_personality("test_p", "Test Personality", "Description", "Prompt")
    p = db.get_personality("test_p")
    assert p is not None
    assert p["name"] == "Test Personality"
    assert p["description"] == "Description"

def test_add_work_and_excerpt(db):
    db.add_personality("test_p", "Test Personality", "Description", "Prompt")
    w_id = db.add_work("test_p", "Test Work", "book", "http://example.com")

    db.add_excerpt(w_id, "This is a test excerpt.", chapter="1", page="10")

    excerpts = db.get_excerpts_by_personality("test_p")
    assert len(excerpts) == 1
    assert excerpts[0]["text"] == "This is a test excerpt."
    assert excerpts[0]["title"] == "Test Work"
    assert excerpts[0]["name"] == "Test Personality"

def test_get_nonexistent_personality(db):
    p = db.get_personality("nonexistent")
    assert p is None
