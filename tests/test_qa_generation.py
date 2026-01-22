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
            # Patch DatabaseManager to use a temporary DB
            from socials_data.core.db import DatabaseManager
            temp_db_path = self.test_dir / "test.db"

            with patch("socials_data.core.processor.DatabaseManager", side_effect=lambda: DatabaseManager(temp_db_path)):
                processor = TextDataProcessor()

                # Run process
                processor.process(self.test_dir)

                # Verify DB
                conn = processor.db.get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM qa_pairs WHERE personality_id = 'test_person'")
                rows = cursor.fetchall()
                conn.close()

                self.assertEqual(len(rows), 1)
                # rows[0] = (id, personality_id, source, question, answer)
                self.assertEqual(rows[0][3], "What is this?")
                self.assertEqual(rows[0][4], "This is a test sentence.")

    @patch("socials_data.core.llm.OpenAI")
    def test_skip_qa(self, MockOpenAI):
         # Setup mock response (should not be called)
        mock_client = MagicMock()
        MockOpenAI.return_value = mock_client

        with patch.dict('os.environ', {'OPENAI_API_KEY': 'fake-key'}):
            # Patch DatabaseManager to use a temporary DB
            from socials_data.core.db import DatabaseManager
            temp_db_path = self.test_dir / "test.db"

            with patch("socials_data.core.processor.DatabaseManager", side_effect=lambda: DatabaseManager(temp_db_path)):
                processor = TextDataProcessor()
                # Run with skip_qa=True
                processor.process(self.test_dir, skip_qa=True)

                # Verify qa_pairs is empty
                conn = processor.db.get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM qa_pairs WHERE personality_id = 'test_person'")
                rows = cursor.fetchall()
                conn.close()

                self.assertEqual(len(rows), 0)

                # Verify mock was NOT called
                mock_client.chat.completions.create.assert_not_called()

if __name__ == "__main__":
    unittest.main()
