import pytest
import sqlite3
from pathlib import Path
from socials_data.core.manager import PersonalityManager

def test_aristotle_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "aristotle" in personalities

def test_aristotle_db_structure():
    base_dir = Path(__file__).parent.parent
    db_path = base_dir / "socials_data" / "personalities" / "aristotle" / "processed" / "aristotle.db"

    assert db_path.exists()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    assert "works" in tables
    assert "quotes" in tables
    assert "concepts" in tables

    # Check data content
    cursor.execute("SELECT term FROM concepts")
    concepts = [row[0] for row in cursor.fetchall()]
    assert "Golden Mean" in concepts
    assert "Eudaimonia" in concepts

    conn.close()
