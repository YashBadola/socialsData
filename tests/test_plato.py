import unittest
import shutil
from pathlib import Path
from socials_data.core.manager import PersonalityManager
from socials_data.core.loader import load_dataset

class TestPlato(unittest.TestCase):
    def setUp(self):
        self.manager = PersonalityManager()
        self.personality_id = "plato"

    def test_metadata_exists(self):
        """Test that metadata.json exists and contains correct fields."""
        metadata = self.manager.get_metadata(self.personality_id)
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata["name"], "Plato")
        self.assertEqual(metadata["id"], "plato")
        self.assertIn("system_prompt", metadata)

    def test_raw_files_exist(self):
        """Test that raw files have been downloaded."""
        raw_dir = self.manager.base_dir / self.personality_id / "raw"
        files = list(raw_dir.iterdir())
        self.assertTrue(len(files) > 0)
        self.assertTrue(any("republic.txt" in f.name for f in files))

    def test_processed_data_exists(self):
        """Test that processed data.jsonl exists."""
        processed_dir = self.manager.base_dir / self.personality_id / "processed"
        data_file = processed_dir / "data.jsonl"
        self.assertTrue(data_file.exists())

    def test_load_dataset(self):
        """Test loading the dataset using load_dataset."""
        # This requires the package to be installed or properly in path
        try:
            dataset = load_dataset(self.personality_id)
            self.assertIsNotNone(dataset)
            # Check if we have some data
            self.assertTrue(len(dataset) > 0)
            sample = dataset[0]
            self.assertIn("text", sample)
            self.assertIn("source", sample)
            # Check for a known phrase from the Republic (e.g., "Socrates", "justice")
            # Since we have the whole text in one chunk (or few), looking for common words is safe.
            # But wait, the processor chunking might be just one big file.
            # Let's check.
            found_keyword = False
            for item in dataset:
                 if "Socrates" in item["text"] or "justice" in item["text"]:
                     found_keyword = True
                     break
            self.assertTrue(found_keyword, "Expected keywords 'Socrates' or 'justice' not found in dataset.")

        except ImportError:
            self.skipTest("datasets library not installed or load_dataset failed")

if __name__ == '__main__':
    unittest.main()
