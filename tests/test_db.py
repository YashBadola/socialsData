import unittest
import os
import sqlite3
from pathlib import Path
from socials_data.core.db import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.test_db_path = Path("test_philosophers.db")
        self.db = Database(self.test_db_path)
        self.db.init_db()

    def tearDown(self):
        self.db.close()
        if self.test_db_path.exists():
            os.remove(self.test_db_path)

    def test_add_personality(self):
        self.db.add_personality("test_p", "Test Personality", "Desc", "Prompt")
        p = self.db.get_personality("test_p")
        self.assertIsNotNone(p)
        self.assertEqual(p['name'], "Test Personality")

    def test_add_document_and_chunk(self):
        self.db.add_personality("test_p", "Test Personality", "", "")
        doc_id = self.db.add_document("test_p", "test.txt", "content")
        chunk_id = self.db.add_chunk(doc_id, "chunk")

        self.db.connect()
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM chunks WHERE id=?", (chunk_id,))
        row = cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row['text'], "chunk")
        self.db.close()

if __name__ == '__main__':
    unittest.main()
