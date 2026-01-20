import unittest
import sqlite3
import shutil
import tempfile
import json
from pathlib import Path
from socials_data.core.db import SocialsDatabase

class TestSocialsDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = str(Path(self.temp_dir) / "test.db")
        self.db = SocialsDatabase(self.db_path)
        self.db.init_db()

        # Create a dummy personality structure
        self.p_dir = Path(self.temp_dir) / "test_personality"
        (self.p_dir / "processed").mkdir(parents=True)

        metadata = {
            "name": "Test Person",
            "id": "test_person",
            "description": "A test personality.",
            "sources": [{"title": "Test Book", "url": "http://example.com", "type": "book"}]
        }
        with open(self.p_dir / "metadata.json", "w") as f:
            json.dump(metadata, f)

        data = [
            {"text": "This is a test chunk.", "source": "test.txt"},
            {"text": "Another chunk of text.", "source": "test.txt"}
        ]
        with open(self.p_dir / "processed" / "data.jsonl", "w") as f:
            for item in data:
                f.write(json.dumps(item) + "\n")

        qa_data = [
            {"question": "What is this?", "answer": "A test.", "source": "test.txt"}
        ]
        with open(self.p_dir / "processed" / "qa.jsonl", "w") as f:
            for item in qa_data:
                f.write(json.dumps(item) + "\n")

    def tearDown(self):
        self.db.close()
        shutil.rmtree(self.temp_dir)

    def test_ingest_and_search(self):
        self.db.ingest_personality("test_personality", self.temp_dir)

        # Verify personality
        self.db.connect()
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM personalities WHERE id='test_person'")
        p = cursor.fetchone()
        self.assertIsNotNone(p)
        self.assertEqual(p['name'], "Test Person")

        # Verify content (2 texts + 1 QA)
        cursor.execute("SELECT * FROM content WHERE personality_id='test_person'")
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 3)

        # Verify QA type
        cursor.execute("SELECT * FROM content WHERE personality_id='test_person' AND type='qa'")
        qa_rows = cursor.fetchall()
        self.assertEqual(len(qa_rows), 1)
        self.assertIn("Q: What is this?", qa_rows[0]['text'])

        # Verify Search
        results = self.db.search("test chunk")
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]['text'], "This is a test chunk.")

if __name__ == '__main__':
    unittest.main()
