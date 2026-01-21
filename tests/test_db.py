import unittest
import tempfile
import os
from socials_data.core.db import SocialsDatabase

class TestSocialsDatabase(unittest.TestCase):
    def setUp(self):
        # Create a temporary file for the database
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.db = SocialsDatabase(self.db_path)
        self.db.init_db()

    def tearDown(self):
        self.db.close()
        os.close(self.db_fd)
        os.remove(self.db_path)

    def test_upsert_personality(self):
        self.db.upsert_personality("test_p", "Test Name", "Desc", "Prompt", {"key": "value"})

        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM personalities WHERE id='test_p'")
        row = cursor.fetchone()
        self.assertEqual(row['name'], "Test Name")
        self.assertEqual(row['description'], "Desc")

        # Update
        self.db.upsert_personality("test_p", "New Name", "Desc", "Prompt")
        cursor.execute("SELECT * FROM personalities WHERE id='test_p'")
        row = cursor.fetchone()
        self.assertEqual(row['name'], "New Name")

    def test_add_content_and_search(self):
        self.db.upsert_personality("test_p", "Test Name", "Desc", "Prompt")
        self.db.add_content("test_p", "This is a unique test content string.", "text")

        results = self.db.search("unique test content")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['text'], "This is a unique test content string.")

    def test_add_source(self):
        self.db.upsert_personality("test_p", "Test Name", "Desc", "Prompt")
        sid = self.db.add_source("test_p", "Test Title", "http://example.com", "book")

        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM sources WHERE id=?", (sid,))
        row = cursor.fetchone()
        self.assertEqual(row['title'], "Test Title")

if __name__ == '__main__':
    unittest.main()
