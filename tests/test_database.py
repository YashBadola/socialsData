import unittest
import sqlite3
from pathlib import Path
from socials_data.core.database import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        # Use a temporary database for testing
        self.test_db_path = Path("tests/test_philosophers.db")
        self.db = DatabaseManager(db_path=str(self.test_db_path))

    def tearDown(self):
        if self.test_db_path.exists():
            self.test_db_path.unlink()

    def test_init_db(self):
        self.assertTrue(self.test_db_path.exists())
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()

        # Check tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='personalities'")
        self.assertIsNotNone(cursor.fetchone())

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sources'")
        self.assertIsNotNone(cursor.fetchone())
        conn.close()

    def test_add_and_get_personality(self):
        data = {
            "id": "test_phil",
            "name": "Test Philosopher",
            "description": "A test philosopher.",
            "system_prompt": "You are a test.",
            "license": "MIT",
            "sources": [
                {"title": "Test Book", "url": "http://example.com", "type": "book"}
            ]
        }

        self.db.add_personality(data)

        p = self.db.get_personality("test_phil")
        self.assertIsNotNone(p)
        self.assertEqual(p['name'], "Test Philosopher")
        self.assertEqual(len(p['sources']), 1)
        self.assertEqual(p['sources'][0]['title'], "Test Book")

    def test_list_personalities(self):
        data1 = {"id": "p1", "name": "P1", "sources": []}
        data2 = {"id": "p2", "name": "P2", "sources": []}

        self.db.add_personality(data1)
        self.db.add_personality(data2)

        plist = self.db.list_personalities()
        self.assertEqual(len(plist), 2)
        self.assertTrue(any(p['id'] == 'p1' for p in plist))
        self.assertTrue(any(p['id'] == 'p2' for p in plist))

if __name__ == '__main__':
    unittest.main()
