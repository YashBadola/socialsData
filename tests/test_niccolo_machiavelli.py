import unittest
import os
import json
from socials_data.personalities.niccolo_machiavelli import metadata_path, processed_data_path
from datasets import load_dataset

class TestNiccoloMachiavelli(unittest.TestCase):
    def test_metadata_exists(self):
        self.assertTrue(os.path.exists(metadata_path))
        with open(metadata_path, 'r') as f:
            data = json.load(f)
        self.assertEqual(data['id'], 'niccolo_machiavelli')
        self.assertIn("The Prince", data['sources'][0]['title'])

    def test_processed_data_exists(self):
        self.assertTrue(os.path.exists(processed_data_path))

    def test_dataset_loading(self):
        # We need to install the package first or ensure PYTHONPATH is set,
        # but in this test environment we assume the package structure is valid.
        # This test mimics how a user would load the dataset.

        # We can't easily use the exported `load_dataset` because it might look for the package installed.
        # However, we can inspect the jsonl directly or try to load it using the huggingface datasets library.

        # Let's try to load it as a JSON dataset
        try:
            dataset = load_dataset('json', data_files=str(processed_data_path), split='train')
            self.assertGreater(len(dataset), 0)
            sample = dataset[0]
            self.assertIn('text', sample)
            self.assertIn('source', sample)
            # Check for a known phrase from Machiavelli
            # Since the chunking might split things up, we search the whole dataset or just check the first chunk
            # if it's large enough. The output showed a large chunk.

            # Searching for "Machiavelli" or "Prince" or specific content in the first few chunks
            found = False
            for i in range(min(5, len(dataset))):
                if "Machiavelli" in dataset[i]['text'] or "Prince" in dataset[i]['text'] or "power" in dataset[i]['text']:
                    found = True
                    break
            self.assertTrue(found, "Did not find expected keywords in the first few samples")

        except Exception as e:
            self.fail(f"Failed to load dataset: {e}")

if __name__ == '__main__':
    unittest.main()
