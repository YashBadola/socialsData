import os
import sqlite3
import pytest
from pathlib import Path
from socials_data.core.db import DatabaseManager
from socials_data.core.manager import PersonalityManager

@pytest.fixture
def db_path(tmp_path):
    """Fixture to create a temporary database."""
    return tmp_path / "test_socials.db"

@pytest.fixture
def db_manager(db_path):
    """Fixture to create a DatabaseManager with a temporary DB."""
    manager = DatabaseManager(db_path=db_path)
    manager.init_db()
    return manager

def test_init_db(db_path, db_manager):
    """Test database initialization."""
    assert db_path.exists()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    assert "personalities" in tables
    assert "content" in tables
    assert "qa_pairs" in tables
    conn.close()

def test_sync_mock(tmp_path):
    """Test syncing with a mock personality structure."""
    # Setup mock personality dir
    personalities_dir = tmp_path / "personalities"
    personalities_dir.mkdir()

    p_dir = personalities_dir / "test_philosopher"
    p_dir.mkdir()
    (p_dir / "processed").mkdir()

    # Create metadata
    with open(p_dir / "metadata.json", "w") as f:
        f.write('{"id": "test_philosopher", "name": "Test Philo", "description": "A test."}')

    # Create data.jsonl
    with open(p_dir / "processed" / "data.jsonl", "w") as f:
        f.write('{"text": "I think therefore I am test.", "source": "test_source"}\n')

    # Initialize Managers with custom paths
    # We need to monkeypatch PersonalityManager's base_dir or instantiate it with one.
    # DatabaseManager instantiates PersonalityManager internally without args.
    # So we need to modify DatabaseManager or patch PersonalityManager.

    # Let's verify DatabaseManager structure.
    # self.personality_manager = PersonalityManager()

    # We can patch the instance's personality_manager
    db_path = tmp_path / "socials.db"
    db_mgr = DatabaseManager(db_path=db_path)
    db_mgr.init_db()

    # Patch the personality manager
    pm = PersonalityManager(base_dir=personalities_dir)
    db_mgr.personality_manager = pm

    # Run sync
    db_mgr.sync_personality("test_philosopher")

    # Verify DB content
    cols, res = db_mgr.query("SELECT * FROM personalities WHERE id='test_philosopher'")
    assert len(res) == 1
    assert res[0][1] == "Test Philo"

    cols, res = db_mgr.query("SELECT * FROM content WHERE personality_id='test_philosopher'")
    assert len(res) == 1
    assert res[0][2] == "I think therefore I am test."
