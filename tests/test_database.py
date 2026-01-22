import unittest
import tempfile
import sqlite3
import shutil
from pathlib import Path
from socials_data.core.database import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / "test_db.sqlite"
        self.db = DatabaseManager(str(self.db_path))

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_add_and_get_personality(self):
        data = {
            "id": "test_phil",
            "name": "Test Philosopher",
            "description": "A test philosopher.",
            "system_prompt": "You are a test.",
            "license": "MIT",
            "sources": [
                {"title": "Book 1", "url": "http://example.com/1", "type": "book"}
            ]
        }

        self.db.add_personality(data)

        retrieved = self.db.get_personality("test_phil")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["name"], "Test Philosopher")
        self.assertEqual(len(retrieved["sources"]), 1)
        self.assertEqual(retrieved["sources"][0]["title"], "Book 1")

    def test_update_personality(self):
        data = {
            "id": "test_phil",
            "name": "Test Philosopher",
            "sources": []
        }
        self.db.add_personality(data)

        # Update
        data["name"] = "Updated Name"
        data["sources"] = [{"title": "New Book", "url": "http://example.com/new", "type": "article"}]
        self.db.add_personality(data)

        retrieved = self.db.get_personality("test_phil")
        self.assertEqual(retrieved["name"], "Updated Name")
        self.assertEqual(len(retrieved["sources"]), 1)
        self.assertEqual(retrieved["sources"][0]["title"], "New Book")

    def test_list_personalities(self):
        self.db.add_personality({"id": "p1", "name": "P1"})
        self.db.add_personality({"id": "p2", "name": "P2"})

        personalities = self.db.list_personalities()
        self.assertEqual(len(personalities), 2)
        ids = [p["id"] for p in personalities]
        self.assertIn("p1", ids)
        self.assertIn("p2", ids)

if __name__ == '__main__':
    unittest.main()
