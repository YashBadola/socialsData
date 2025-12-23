
import unittest
from socials_data.core.loader import load_dataset
import os
import json

class TestNiccoloMachiavelli(unittest.TestCase):
    def test_load_dataset(self):
        # Ensure the dataset loads without error
        dataset = load_dataset("niccolo_machiavelli")
        self.assertIsNotNone(dataset)
        self.assertGreater(len(dataset), 0)

    def test_content_check(self):
        dataset = load_dataset("niccolo_machiavelli")

        # Check for keywords from The Prince
        prince_keywords = ["prince", "principality", "fortune", "virtu", "cesare borgia"]
        found_prince = False

        # Check for keywords from Discourses
        discourses_keywords = ["republic", "rome", "liberty", "titus livius"]
        found_discourses = False

        for item in dataset:
            text = item["text"].lower()
            if any(k in text for k in prince_keywords):
                found_prince = True
            if any(k in text for k in discourses_keywords):
                found_discourses = True

            if found_prince and found_discourses:
                break

        self.assertTrue(found_prince, "Did not find keywords from The Prince")
        self.assertTrue(found_discourses, "Did not find keywords from Discourses")

    def test_metadata(self):
        metadata_path = os.path.join("socials_data", "personalities", "niccolo_machiavelli", "metadata.json")
        with open(metadata_path, "r") as f:
            metadata = json.load(f)

        self.assertEqual(metadata["id"], "niccolo_machiavelli")
        self.assertIn("The Prince", [s["title"] for s in metadata["sources"]])

if __name__ == "__main__":
    unittest.main()
