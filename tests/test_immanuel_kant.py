
import unittest
from pathlib import Path
import json
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

class TestImmanuelKant(unittest.TestCase):
    def setUp(self):
        self.manager = PersonalityManager()
        self.personality_id = "immanuel_kant"
        self.personality_dir = self.manager.base_dir / self.personality_id

    def test_metadata(self):
        metadata = self.manager.get_metadata(self.personality_id)
        self.assertEqual(metadata["name"], "Immanuel Kant")
        self.assertEqual(metadata["id"], "immanuel_kant")
        self.assertIn("Enlightenment", metadata["system_prompt"] + metadata["description"])

    def test_raw_files_exist(self):
        raw_dir = self.personality_dir / "raw"
        self.assertTrue(any(raw_dir.iterdir()), "No raw files found")

    def test_processed_files_exist(self):
        processed_dir = self.personality_dir / "processed"
        self.assertTrue((processed_dir / "data.jsonl").exists())

    def test_data_content(self):
        # Verify using the loader
        ds = load_dataset(self.personality_id)
        self.assertTrue(len(ds) > 0)
        sample = ds[0]
        self.assertIn("text", sample)
        # Check for key terms likely to be in the first chunk or early chunks
        # Note: Since the file is large, it might be split.
        # Let's just check type is string and non-empty.
        self.assertIsInstance(sample["text"], str)
        self.assertTrue(len(sample["text"]) > 0)

if __name__ == "__main__":
    unittest.main()
