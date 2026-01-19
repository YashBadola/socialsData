import unittest
import sqlite3
import os
from socials_data.core.db import SocialsDatabase

class TestSocialsDatabase(unittest.TestCase):
    def setUp(self):
        # Use in-memory DB for testing
        self.db_path = ":memory:"
        self.db = SocialsDatabase(self.db_path)
        self.db.init_db()

    def tearDown(self):
        self.db.close()

    def test_upsert_personality(self):
        self.db.upsert_personality("test_p", "Test Personality", "Desc", "Prompt", {"key": "val"})

        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM personalities WHERE id = ?", ("test_p",))
        row = cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row['name'], "Test Personality")

    def test_add_content_and_search(self):
        self.db.upsert_personality("test_p", "Test Personality", "Desc", "Prompt")
        self.db.add_content("test_p", "This is a test content about philosophy.", "text")

        results = self.db.search("philosophy")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['text'], "This is a test content about philosophy.")

        results = self.db.search("banana")
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()
