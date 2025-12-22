import unittest
import os
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

class TestNiccoloMachiavelli(unittest.TestCase):
    def test_dataset_loading(self):
        """Test that the dataset loads correctly and contains data."""
        # Ensure data exists (it should have been processed in the plan)
        processed_file = "socials_data/personalities/niccolo_machiavelli/processed/data.jsonl"
        if not os.path.exists(processed_file):
            self.fail(f"Processed file {processed_file} does not exist. Did you run the processing step?")

        try:
            dataset = load_dataset("niccolo_machiavelli")
        except Exception as e:
            self.fail(f"Failed to load dataset: {e}")

        self.assertTrue(len(dataset) > 0)

        # Check a sample
        sample = dataset[0]
        self.assertIn("text", sample)
        self.assertIsInstance(sample["text"], str)
        self.assertTrue(len(sample["text"]) > 0)

        # Check for keywords
        # Depending on how the text is chunked, "Prince" might not be in every chunk,
        # so we check if it appears in a reasonable subset or the whole dataset combined.
        # Checking the first 100 entries or so should be enough to find relevant terms.
        text_content = [d["text"].lower() for d in dataset.select(range(min(len(dataset), 100)))]

        keywords = ["prince", "state", "fortune", "virtue", "virtù", "italy", "duke", "people"]
        found = False
        for k in keywords:
            if any(k in t for t in text_content):
                found = True
                break
        self.assertTrue(found, f"None of the keywords {keywords} found in the first 100 samples.")

    def test_metadata(self):
        """Test that metadata is correct."""
        manager = PersonalityManager()
        metadata = manager.get_metadata("niccolo_machiavelli")
        self.assertEqual(metadata["name"], "Niccolò Machiavelli")
        self.assertIn("The Prince", [s["title"] for s in metadata["sources"]])

if __name__ == "__main__":
    unittest.main()
