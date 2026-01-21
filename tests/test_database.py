import unittest
import sqlite3
import shutil
import tempfile
from pathlib import Path
from socials_data.core.database import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for the database
        self.test_dir = tempfile.mkdtemp()
        self.db_path = Path(self.test_dir) / "test_philosophers.db"
        self.db = DatabaseManager(db_path=str(self.db_path))

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_add_and_get_personality(self):
        personality_data = {
            "id": "test_philosopher",
            "name": "Test Philosopher",
            "description": "A test description.",
            "system_prompt": "You are a test.",
            "license": "MIT",
            "sources": [
                {"title": "Test Book", "url": "http://example.com", "type": "book"}
            ]
        }

        self.db.add_personality(personality_data)

        retrieved = self.db.get_personality("test_philosopher")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["name"], "Test Philosopher")
        self.assertEqual(retrieved["description"], "A test description.")
        self.assertEqual(len(retrieved["sources"]), 1)
        self.assertEqual(retrieved["sources"][0]["title"], "Test Book")

    def test_list_personalities(self):
        p1 = {"id": "p1", "name": "P1"}
        p2 = {"id": "p2", "name": "P2"}

        self.db.add_personality(p1)
        self.db.add_personality(p2)

        personalities = self.db.list_personalities()
        self.assertEqual(len(personalities), 2)
        ids = [p["id"] for p in personalities]
        self.assertIn("p1", ids)
        self.assertIn("p2", ids)

    def test_update_personality(self):
        p1 = {"id": "p1", "name": "P1", "sources": [{"title": "Old Source"}]}
        self.db.add_personality(p1)

        p1_updated = {"id": "p1", "name": "P1 Updated", "sources": [{"title": "New Source"}]}
        self.db.add_personality(p1_updated)

        retrieved = self.db.get_personality("p1")
        self.assertEqual(retrieved["name"], "P1 Updated")
        self.assertEqual(len(retrieved["sources"]), 1)
        self.assertEqual(retrieved["sources"][0]["title"], "New Source")

if __name__ == '__main__':
    unittest.main()
