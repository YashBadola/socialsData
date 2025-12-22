import unittest
import os
import json
from socials_data.core.manager import PersonalityManager

class TestPlato(unittest.TestCase):
    def setUp(self):
        self.manager = PersonalityManager()
        self.personality_id = "plato"
        self.base_dir = self.manager.base_dir / self.personality_id

    def test_metadata_exists(self):
        """Test that metadata.json exists and contains correct info."""
        metadata = self.manager.get_metadata(self.personality_id)
        self.assertEqual(metadata["name"], "Plato")
        self.assertEqual(metadata["id"], "plato")
        self.assertIn("Socrates", metadata["description"])
        self.assertTrue(len(metadata["sources"]) >= 2)

    def test_raw_files_exist(self):
        """Test that raw text files exist."""
        raw_dir = self.base_dir / "raw"
        self.assertTrue((raw_dir / "republic.txt").exists())
        self.assertTrue((raw_dir / "apology.txt").exists())

    def test_processed_data_exists(self):
        """Test that processed data.jsonl exists and has content."""
        data_file = self.base_dir / "processed" / "data.jsonl"
        self.assertTrue(data_file.exists())

        with open(data_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            self.assertTrue(len(lines) > 0)

            # Check the first line for basic structure
            first_entry = json.loads(lines[0])
            self.assertIn("text", first_entry)
            self.assertIn("source", first_entry)
            # The text should be substantial
            self.assertTrue(len(first_entry["text"]) > 100)

    def test_content_keywords(self):
        """Test that the content actually looks like Plato."""
        data_file = self.base_dir / "processed" / "data.jsonl"
        found_socrates = False
        found_athens = False

        with open(data_file, 'r', encoding='utf-8') as f:
            for line in f:
                entry = json.loads(line)
                text = entry["text"]
                if "Socrates" in text:
                    found_socrates = True
                if "Athens" in text or "Athenians" in text:
                    found_athens = True
                if found_socrates and found_athens:
                    break

        self.assertTrue(found_socrates, "Should mention Socrates")
        self.assertTrue(found_athens, "Should mention Athens")

if __name__ == "__main__":
    unittest.main()
