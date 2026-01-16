import unittest
import sqlite3
import shutil
import json
from pathlib import Path
from socials_data.core.db import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("test_data")
        self.test_dir.mkdir(exist_ok=True)
        self.db_path = self.test_dir / "test_socials.db"
        self.manager = DatabaseManager(str(self.db_path))
        self.manager.connect()

    def tearDown(self):
        self.manager.close()
        shutil.rmtree(self.test_dir)

    def test_create_tables(self):
        cursor = self.manager.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        self.assertIn('philosophers', tables)
        self.assertIn('works', tables)
        self.assertIn('segments', tables)
        self.assertIn('qa_pairs', tables)

    def test_add_philosopher(self):
        metadata = {
            "id": "test_phil",
            "name": "Test Phil",
            "description": "A test philosopher",
            "license": "MIT",
            "sources": [{"title": "Test Work", "url": "http://example.com"}]
        }
        self.manager.add_philosopher(metadata)

        cursor = self.manager.conn.cursor()
        cursor.execute("SELECT * FROM philosophers WHERE id='test_phil'")
        phil = cursor.fetchone()
        self.assertIsNotNone(phil)
        self.assertEqual(phil[1], "Test Phil")

        cursor.execute("SELECT * FROM works WHERE philosopher_id='test_phil'")
        work = cursor.fetchone()
        self.assertIsNotNone(work)
        self.assertEqual(work[2], "Test Work")

    def test_add_segments(self):
        # Create a dummy philosopher first
        metadata = {"id": "test_phil", "name": "Test Phil"}
        self.manager.add_philosopher(metadata)

        # Create dummy jsonl
        jsonl_path = self.test_dir / "data.jsonl"
        with open(jsonl_path, "w") as f:
            f.write(json.dumps({"text": "Hello world", "source": "test.txt"}) + "\n")
            f.write(json.dumps({"text": "Another line", "source": "test.txt"}) + "\n")

        self.manager.add_segments("test_phil", jsonl_path)

        cursor = self.manager.conn.cursor()
        cursor.execute("SELECT * FROM segments WHERE philosopher_id='test_phil'")
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][2], "Hello world")

if __name__ == '__main__':
    unittest.main()
