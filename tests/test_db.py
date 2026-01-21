import pytest
import os
from socials_data.core.db import DatabaseManager

@pytest.fixture
def db_path(tmp_path):
    return tmp_path / "test_socials.db"

def test_database_creation(db_path):
    db = DatabaseManager(str(db_path))
    assert os.path.exists(db_path)

def test_add_and_get_personality(db_path):
    db = DatabaseManager(str(db_path))
    db.add_personality("test_p", "Test Personality", "Description", "Prompt")

    p = db.get_personality("test_p")
    assert p is not None
    assert p[0] == "test_p"
    assert p[1] == "Test Personality"

def test_add_and_get_excerpt(db_path):
    db = DatabaseManager(str(db_path))
    db.add_personality("test_p", "Test Personality", "Description", "Prompt")
    db.add_excerpt("test_p", "This is a test excerpt.")

    excerpts = db.get_excerpts("test_p")
    assert len(excerpts) == 1
    assert excerpts[0] == "This is a test excerpt."
