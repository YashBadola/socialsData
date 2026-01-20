import sqlite3
import unittest
import os
from socials_data.core.db import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.test_db_path = "test_philosophers.db"
        self.db = DatabaseManager(db_path=self.test_db_path)

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_add_and_get_personality(self):
        self.db.add_personality(
            id="test_pers",
            name="Test Name",
            description="Test Description",
            system_prompt="You are a test.",
            license="MIT"
        )

        pers = self.db.get_personality("test_pers")
        self.assertIsNotNone(pers)
        self.assertEqual(pers["name"], "Test Name")
        self.assertEqual(pers["description"], "Test Description")

    def test_add_and_get_chunks(self):
        self.db.add_personality("test_pers", "Test", "Desc", "Prompt", "Lic")
        self.db.add_chunk("test_pers", "source.txt", "This is a chunk.")

        chunks = self.db.get_chunks("test_pers")
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0]["text"], "This is a chunk.")
        self.assertEqual(chunks[0]["source"], "source.txt")

if __name__ == '__main__':
    unittest.main()
