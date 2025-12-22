import unittest
import os
from socials_data import load_dataset

class TestMachiavelli(unittest.TestCase):
    def test_load_dataset(self):
        # Load the dataset for Niccolò Machiavelli
        dataset = load_dataset("niccolo_machiavelli")

        # Check if the dataset is not empty
        self.assertTrue(len(dataset) > 0, "Dataset should not be empty")

        # Verify columns
        self.assertIn("text", dataset.column_names, "Dataset should contain 'text' column")
        self.assertIn("source", dataset.column_names, "Dataset should contain 'source' column")

        # Check for relevant keywords in the text
        # Since we processed "The Prince", we expect words like "prince", "state", "virtue" (or virtù), "fortune"
        found_keyword = False
        keywords = ["prince", "state", "fortune", "virtue", "medici", "republic"]

        # Iterate through a few samples (it might be large, so just check the first few)
        for i in range(min(10, len(dataset))):
            text = dataset[i]["text"].lower()
            if any(k in text for k in keywords):
                found_keyword = True
                break

        self.assertTrue(found_keyword, f"Should find one of {keywords} in the dataset samples")

if __name__ == "__main__":
    unittest.main()
