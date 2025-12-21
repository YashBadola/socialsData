import unittest
import shutil
import json
from pathlib import Path
from socials_data.core.loader import load_dataset
from datasets import Dataset

class TestLoader(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("socials_data/personalities/test_loader_person")
        self.processed_dir = self.test_dir / "processed"
        self.processed_dir.mkdir(parents=True, exist_ok=True)

        # Create dummy data.jsonl
        with open(self.processed_dir / "data.jsonl", "w") as f:
            f.write(json.dumps({"text": "Hello world", "source": "test"}) + "\n")

        # Create dummy qa.jsonl
        with open(self.processed_dir / "qa.jsonl", "w") as f:
            f.write(json.dumps({"instruction": "Hi?", "response": "Hello world", "source": "test"}) + "\n")

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_load_text(self):
        ds = load_dataset("test_loader_person", data_type="text")
        self.assertIsInstance(ds, Dataset)
        self.assertEqual(len(ds), 1)
        self.assertEqual(ds[0]["text"], "Hello world")

    def test_load_qa(self):
        ds = load_dataset("test_loader_person", data_type="qa")
        self.assertIsInstance(ds, Dataset)
        self.assertEqual(len(ds), 1)
        self.assertEqual(ds[0]["instruction"], "Hi?")
        self.assertEqual(ds[0]["response"], "Hello world")

    def test_load_missing(self):
        with self.assertRaises(FileNotFoundError):
            load_dataset("non_existent_person")

    def test_load_missing_qa(self):
        # Remove qa file
        (self.processed_dir / "qa.jsonl").unlink()
        with self.assertRaises(FileNotFoundError):
            load_dataset("test_loader_person", data_type="qa")

if __name__ == "__main__":
    unittest.main()
