import unittest
from unittest.mock import MagicMock, patch
import json
import shutil
from pathlib import Path
from socials_data.core.processor import TextDataProcessor
from socials_data.core.llm import LLMProcessor

class TestQAGeneration(unittest.TestCase):
    def setUp(self):
        # Create a temp personality directory
        self.test_dir = Path("tests/temp_personality")
        self.raw_dir = self.test_dir / "raw"
        self.processed_dir = self.test_dir / "processed"

        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

        # Create metadata
        with open(self.test_dir / "metadata.json", "w") as f:
            json.dump({
                "name": "Test Person",
                "id": "test_person",
                "system_prompt": "You are a test."
            }, f)

        # Create raw file
        with open(self.raw_dir / "test.txt", "w") as f:
            f.write("This is a test sentence.")

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    @patch("socials_data.core.llm.OpenAI")
    def test_qa_generation_mock(self, MockOpenAI):
        # Setup mock response
        mock_client = MagicMock()
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = '[{"instruction": "What is this?", "response": "This is a test sentence."}]'
        mock_client.chat.completions.create.return_value = mock_completion
        MockOpenAI.return_value = mock_client

        # Initialize processor
        # We need to force LLMProcessor to accept the mock even if env var is missing
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'fake-key'}):
            processor = TextDataProcessor()

            # Run process
            processor.process(self.test_dir)

            # Verify qa.jsonl
            qa_file = self.processed_dir / "qa.jsonl"
            self.assertTrue(qa_file.exists())

            with open(qa_file, "r") as f:
                lines = f.readlines()
                self.assertEqual(len(lines), 1)
                data = json.loads(lines[0])
                self.assertEqual(data["instruction"], "What is this?")
                self.assertEqual(data["response"], "This is a test sentence.")
                self.assertEqual(data["source"], "test.txt")

    @patch("socials_data.core.llm.OpenAI")
    def test_skip_qa(self, MockOpenAI):
         # Setup mock response (should not be called)
        mock_client = MagicMock()
        MockOpenAI.return_value = mock_client

        with patch.dict('os.environ', {'OPENAI_API_KEY': 'fake-key'}):
            processor = TextDataProcessor()
            # Run with skip_qa=True
            processor.process(self.test_dir, skip_qa=True)

            # Verify qa.jsonl is empty or not written to
            qa_file = self.processed_dir / "qa.jsonl"
            # In current implementation, we open it with 'w', so it exists but empty?
            # Actually, if we skip_qa, we never write to it, but we might have opened it?
            # Let's check the logic: "if not skip_qa: qa_f = open..."
            # So if skip_qa is True, qa_f is never created/touched.
            # But wait, my implementation:
            # if not skip_qa: qa_f = open(...)
            # So the file might NOT exist if it didn't before.
            # But "processed_dir" is cleaned/created.

            # Since we just created the dir in setUp, and process() with skip_qa=True
            # won't create qa.jsonl, it should not exist.
            self.assertFalse(qa_file.exists())

            # Verify mock was NOT called
            mock_client.chat.completions.create.assert_not_called()

if __name__ == "__main__":
    unittest.main()
