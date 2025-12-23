
import unittest
from socials_data.core.loader import load_dataset
import os
import json

class TestThomasHobbes(unittest.TestCase):
    def setUp(self):
        self.personality_id = 'thomas_hobbes'
        self.base_dir = os.path.join(os.path.dirname(__file__), '..', 'socials_data', 'personalities', self.personality_id)

    def test_metadata_exists(self):
        metadata_path = os.path.join(self.base_dir, 'metadata.json')
        self.assertTrue(os.path.exists(metadata_path))
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        self.assertEqual(metadata['id'], self.personality_id)
        self.assertIn('Leviathan', metadata['sources'][0]['title'])

    def test_raw_file_exists(self):
        raw_path = os.path.join(self.base_dir, 'raw', 'leviathan.txt')
        self.assertTrue(os.path.exists(raw_path))

    def test_processed_files_exist(self):
        processed_dir = os.path.join(self.base_dir, 'processed')
        self.assertTrue(os.path.exists(os.path.join(processed_dir, 'data.jsonl')))
        # qa.jsonl might exist but be empty if no API key, but the file should be there or not depending on implementation
        # The output said "Done. Data saved..." and "Info: No Q&A generated".
        # Let's check data.jsonl content

    def test_load_dataset(self):
        # Test loading via the package function
        dataset = load_dataset(self.personality_id)
        self.assertIsNotNone(dataset)
        # Check that we have some data
        self.assertGreater(len(dataset), 0)

        # Check a sample
        sample = dataset[0]
        self.assertIn('text', sample)
        self.assertIn('source', sample)
        self.assertEqual(sample['source'], 'leviathan.txt')

        # Check content relevance (look for "leviathan" or "common-wealth" or "sovereign" in the first few chunks)
        # We can't guarantee which chunk is first, but we can search the dataset
        found_keyword = False
        for item in dataset:
            text = item['text'].lower()
            if 'leviathan' in text or 'common-wealth' in text or 'sovereign' in text:
                found_keyword = True
                break
        self.assertTrue(found_keyword, "Key terms not found in dataset")

if __name__ == '__main__':
    unittest.main()
