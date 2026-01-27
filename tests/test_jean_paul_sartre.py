import unittest
from socials_data import load_dataset
import os

class TestJeanPaulSartre(unittest.TestCase):
    def test_load_dataset(self):
        # Load the dataset
        ds = load_dataset("jean_paul_sartre")

        # Check if we have data
        self.assertGreater(len(ds), 0, "Dataset should not be empty")

        # Check if the content is correct
        all_text = " ".join([item["text"] for item in ds])

        # Check for key phrases from our raw files
        self.assertIn("Existence Precedes Essence", all_text)
        self.assertIn("Hell is other people", all_text)
        self.assertIn("Jean-Paul Charles Aymard Sartre", all_text)
        self.assertIn("Bad Faith", all_text)

if __name__ == "__main__":
    unittest.main()
