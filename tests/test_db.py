import unittest
import os
from socials_data.core.db import SocialsDatabase
import shutil
from pathlib import Path
import json

class TestSocialsDatabase(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_socials.db"
        self.db = SocialsDatabase(self.db_path)
        self.db.connect()

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_add_personality(self):
        meta = {
            "id": "test_person",
            "name": "Test Person",
            "description": "A test personality",
            "system_prompt": "You are a test."
        }
        self.db.add_personality(meta)

        personalities = self.db.get_personalities()
        self.assertEqual(len(personalities), 1)
        self.assertEqual(personalities[0][0], "test_person")
        self.assertEqual(personalities[0][1], "Test Person")

    def test_add_content(self):
        meta = {
            "id": "test_person",
            "name": "Test Person"
        }
        self.db.add_personality(meta)

        self.db.add_content("test_person", "Some content", "text")

        results = self.db.search_content("content")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][3], "Some content")

if __name__ == "__main__":
    unittest.main()
