import unittest
import os
import json
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset

class TestPlato(unittest.TestCase):
    def setUp(self):
        self.manager = PersonalityManager()
        self.personality_id = "plato"

    def test_metadata_exists(self):
        """Test that metadata exists and is correct."""
        metadata = self.manager.get_metadata(self.personality_id)
        self.assertEqual(metadata["name"], "Plato")
        self.assertEqual(metadata["id"], "plato")
        self.assertTrue("system_prompt" in metadata)

    def test_raw_files_exist(self):
        """Test that raw files were downloaded."""
        personality_dir = self.manager.base_dir / self.personality_id
        raw_dir = personality_dir / "raw"
        self.assertTrue((raw_dir / "republic.txt").exists())
        self.assertTrue((raw_dir / "symposium.txt").exists())
        self.assertTrue((raw_dir / "phaedo.txt").exists())

    def test_processed_data_exists(self):
        """Test that processed data was generated."""
        personality_dir = self.manager.base_dir / self.personality_id
        processed_file = personality_dir / "processed" / "data.jsonl"
        self.assertTrue(processed_file.exists())
        self.assertGreater(processed_file.stat().st_size, 0)

    def test_load_dataset_integration(self):
        """Test loading the dataset via the main entry point."""
        try:
            ds = load_dataset(self.personality_id)
            self.assertTrue(len(ds) > 0)
            sample = ds[0]
            self.assertIn("text", sample)
            self.assertIn("source", sample)
        except Exception as e:
            self.fail(f"load_dataset failed: {e}")

if __name__ == "__main__":
    unittest.main()
