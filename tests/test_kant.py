
import unittest
from socials_data import load_dataset
import os

class TestKantDataset(unittest.TestCase):
    def test_load_kant(self):
        try:
            dataset = load_dataset("immanuel_kant")
            self.assertIsNotNone(dataset)
            self.assertGreater(len(dataset), 0)
            print(f"Loaded dataset with {len(dataset)} entries.")

            # Check content
            entry = dataset[0]
            self.assertIn("text", entry)
            self.assertIn("source", entry)
            self.assertTrue("experience" in entry["text"] or "good will" in entry["text"] or "Pure" in entry["text"])

        except Exception as e:
            self.fail(f"Failed to load dataset: {e}")

if __name__ == '__main__':
    unittest.main()
