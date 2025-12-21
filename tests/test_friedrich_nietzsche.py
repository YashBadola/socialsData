import unittest
import json
import os
from pathlib import Path
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

class TestFriedrichNietzsche(unittest.TestCase):
    def setUp(self):
        self.manager = PersonalityManager()
        self.personality_id = "friedrich_nietzsche"
        self.processed_file = Path(f"socials_data/personalities/{self.personality_id}/processed/data.jsonl")

    def test_metadata_exists(self):
        metadata = self.manager.get_metadata(self.personality_id)
        self.assertEqual(metadata["name"], "Friedrich Nietzsche")
        self.assertEqual(metadata["id"], "friedrich_nietzsche")

    def test_processed_data_exists(self):
        self.assertTrue(self.processed_file.exists())
        with open(self.processed_file, "r") as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 0)
            data = json.loads(lines[0])
            self.assertIn("Zarathustra", data["text"])
            self.assertEqual(data["source"], "zarathustra_prologue.txt")

if __name__ == "__main__":
    unittest.main()
