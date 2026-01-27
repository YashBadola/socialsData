from socials_data import load_dataset
import unittest

class TestWittgenstein(unittest.TestCase):
    def test_load_dataset(self):
        dataset = load_dataset("ludwig_wittgenstein")
        self.assertTrue(len(dataset) > 0)
        entry = dataset[0]
        self.assertIn("text", entry)
        self.assertIn("Tractatus Logico-Philosophicus", entry["text"])
        self.assertIn("Philosophical Investigations", entry["text"])

if __name__ == '__main__':
    unittest.main()
