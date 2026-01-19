import pytest
import sqlite3
import tempfile
from pathlib import Path
from socials_data.core.database import DatabaseManager

class TestDatabaseManager:
    @pytest.fixture
    def db_manager(self):
        # Create a temporary file for the database
        with tempfile.NamedTemporaryFile(suffix=".db") as tmp_db:
            # We need the path, but NamedTemporaryFile deletes on close by default.
            # We'll rely on the fact that DatabaseManager will create the file if it doesn't exist.
            # However, since NamedTemporaryFile creates the file, we can just use it.
            # But on Windows this might be an issue if opened twice.
            # A safer way is using tempfile.TemporaryDirectory.
            pass

        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = Path(tmp_dir) / "test.db"
            db = DatabaseManager(db_path=db_path)
            yield db

    def test_init_db(self, db_manager):
        conn = db_manager.get_connection()
        cursor = conn.cursor()

        # Check tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='personalities'")
        assert cursor.fetchone() is not None

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sources'")
        assert cursor.fetchone() is not None
        conn.close()

    def test_add_and_get_personality(self, db_manager):
        personality_data = {
            "id": "test_phil",
            "name": "Test Philosopher",
            "description": "A test philosopher.",
            "system_prompt": "You are a test.",
            "sources": [
                {"title": "Test Book", "url": "http://example.com", "type": "book"}
            ]
        }

        db_manager.add_personality(personality_data)

        retrieved = db_manager.get_personality("test_phil")
        assert retrieved is not None
        assert retrieved["name"] == "Test Philosopher"
        assert retrieved["description"] == "A test philosopher."
        assert len(retrieved["sources"]) == 1
        assert retrieved["sources"][0]["title"] == "Test Book"

    def test_list_personalities(self, db_manager):
        p1 = {"id": "p1", "name": "P1", "sources": []}
        p2 = {"id": "p2", "name": "P2", "sources": []}

        db_manager.add_personality(p1)
        db_manager.add_personality(p2)

        personalities = db_manager.list_personalities()
        assert len(personalities) == 2
        ids = [p["id"] for p in personalities]
        assert "p1" in ids
        assert "p2" in ids

    def test_update_personality(self, db_manager):
        p1 = {"id": "p1", "name": "P1", "sources": [{"title": "Old Source"}]}
        db_manager.add_personality(p1)

        p1_update = {"id": "p1", "name": "P1 Updated", "sources": [{"title": "New Source"}]}
        db_manager.add_personality(p1_update)

        retrieved = db_manager.get_personality("p1")
        assert retrieved["name"] == "P1 Updated"
        assert len(retrieved["sources"]) == 1
        assert retrieved["sources"][0]["title"] == "New Source"
