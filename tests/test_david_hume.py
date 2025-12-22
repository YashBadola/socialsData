import unittest
import os
import json
from socials_data.core.loader import load_dataset

class TestDavidHume(unittest.TestCase):
    def test_load_dataset(self):
        dataset = load_dataset('david_hume')
        self.assertIsNotNone(dataset)
        # Check if we have some data
        self.assertGreater(len(dataset), 0)

        # Check first entry structure
        first_entry = dataset[0]
        self.assertIn('text', first_entry)
        self.assertIn('source', first_entry)

        # Check content
        # We expect some key terms from Hume
        text_sample = first_entry['text']
        self.assertIsInstance(text_sample, str)
        self.assertTrue(len(text_sample) > 0)

    def test_metadata(self):
        meta_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../socials_data/personalities/david_hume/metadata.json')
        with open(meta_path, 'r') as f:
            meta = json.load(f)

        self.assertEqual(meta['id'], 'david_hume')
        self.assertEqual(meta['name'], 'David Hume')
        self.assertIn('Public Domain', meta['license'])

if __name__ == '__main__':
    unittest.main()
