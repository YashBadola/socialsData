import json
from pathlib import Path
import os
import logging
from socials_data.core.llm import LLMProcessor
from socials_data.core.db import DatabaseManager

class DataProcessor:
    def __init__(self):
        self.llm_processor = LLMProcessor()
        self.db = DatabaseManager()

    def process(self, personality_dir, skip_qa=False):
        """
        Reads files from raw/, processes them, and writes to database.
        If skip_qa is False, it also attempts to generate Q&A pairs.
        """
        personality_dir = Path(personality_dir)
        raw_dir = personality_dir / "raw"

        metadata_file = personality_dir / "metadata.json"
        system_prompt = None
        personality_id = personality_dir.name

        if metadata_file.exists():
            try:
                with open(metadata_file, "r") as f:
                    meta = json.load(f)
                    system_prompt = meta.get("system_prompt")
                    # Ensure metadata is synced
                    self.db.upsert_personality(meta)
                    personality_id = meta.get("id", personality_id)
            except Exception as e:
                logging.error(f"Failed to read metadata: {e}")

        # Clear existing data for this personality
        self.db.clear_processed_data(personality_id)

        for file_path in raw_dir.iterdir():
            if file_path.is_file():
                content = self._process_file(file_path)
                if content:
                    # 1. Write standard text data
                    chunks = content if isinstance(content, list) else [content]

                    for chunk in chunks:
                        self.db.insert_processed_data(personality_id, chunk, file_path.name)

                        # 2. If we have a system prompt and valid text, generate Q&A
                        if not skip_qa and system_prompt and self.llm_processor.client:
                            print(f"Generating Q&A for {file_path.name}...") # User feedback
                            qa_pairs = self.llm_processor.generate_qa_pairs(chunk, system_prompt)
                            for pair in qa_pairs:
                                self.db.insert_qa_pair(personality_id, file_path.name, pair["instruction"], pair["response"])

    def generate_qa_only(self, personality_dir):
        """
        Generates Q&A pairs from existing data in database.
        Useful if one wants to run QA generation separately or re-run it.
        """
        personality_dir = Path(personality_dir)

        metadata_file = personality_dir / "metadata.json"
        system_prompt = None
        personality_id = personality_dir.name

        if metadata_file.exists():
            try:
                with open(metadata_file, "r") as f:
                    meta = json.load(f)
                    system_prompt = meta.get("system_prompt")
                    personality_id = meta.get("id", personality_id)
            except Exception as e:
                logging.error(f"Failed to read metadata: {e}")
                return

        if not system_prompt:
            print("No 'system_prompt' found in metadata. Cannot generate Q&A.")
            return

        if not self.llm_processor.client:
            print("No OpenAI API Key found. Cannot generate Q&A.")
            return

        print(f"Generating Q&A from existing data for {personality_id}...")

        # Clear existing QA
        self.db.clear_qa_pairs(personality_id)

        # Get data from DB
        processed_data = self.db.get_processed_data(personality_id)

        if not processed_data:
             print("No processed data found. Run 'process' first.")
             return

        for text, source in processed_data:
            qa_pairs = self.llm_processor.generate_qa_pairs(text, system_prompt)
            for pair in qa_pairs:
                self.db.insert_qa_pair(personality_id, source, pair["instruction"], pair["response"])

        print(f"Done. Q&A saved to database.")


    def _process_file(self, file_path):
        raise NotImplementedError("Subclasses must implement _process_file")

class TextDataProcessor(DataProcessor):
    def _process_file(self, file_path):
        """
        Handles text files. Returns the content as a string.
        """
        # Basic extensions check
        if file_path.suffix.lower() not in ['.txt', '.md']:
            # In a real system, we might log a warning or have other processors
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            # Basic cleaning: collapse multiple newlines, strip whitespace
            # This can be made more sophisticated
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            cleaned_text = "\n".join(lines)

            # Simple chunking if text is too large could be added here
            # For now, we return the whole cleaned text as one chunk
            return cleaned_text
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None

# Future placeholders for other types
class AudioDataProcessor(DataProcessor):
    def _process_file(self, file_path):
        # TODO: Implement Whisper or other transcription logic here
        pass
