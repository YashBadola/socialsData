import json
from pathlib import Path
import os
import logging
from socials_data.core.llm import LLMProcessor

class DataProcessor:
    def __init__(self):
        self.llm_processor = LLMProcessor()

    def process(self, personality_dir):
        """
        Reads files from raw/, processes them, and writes to processed/data.jsonl.
        Also attempts to generate Q&A pairs if system_prompt is present in metadata.
        """
        personality_dir = Path(personality_dir)
        raw_dir = personality_dir / "raw"
        processed_dir = personality_dir / "processed"
        output_file = processed_dir / "data.jsonl"
        qa_output_file = processed_dir / "qa.jsonl"

        metadata_file = personality_dir / "metadata.json"
        system_prompt = None
        if metadata_file.exists():
            try:
                with open(metadata_file, "r") as f:
                    meta = json.load(f)
                    system_prompt = meta.get("system_prompt")
            except Exception as e:
                logging.error(f"Failed to read metadata: {e}")

        processed_dir.mkdir(parents=True, exist_ok=True)

        # Prepare files
        # We overwrite to ensure clean state.
        with open(output_file, "w", encoding="utf-8") as out_f, \
             open(qa_output_file, "w", encoding="utf-8") as qa_f:

            for file_path in raw_dir.iterdir():
                if file_path.is_file():
                    content = self._process_file(file_path)
                    if content:
                        # 1. Write standard text data
                        # TextDataProcessor returns a single string, so we listify it for generic handling
                        # unless it's already a list (which `_process_file` might return in future)
                        chunks = content if isinstance(content, list) else [content]

                        for chunk in chunks:
                            record = {"text": chunk, "source": file_path.name}
                            out_f.write(json.dumps(record) + "\n")

                            # 2. If we have a system prompt and valid text, generate Q&A
                            if system_prompt and self.llm_processor.client:
                                print(f"Generating Q&A for {file_path.name}...") # User feedback
                                # Chunking for QA generation to avoid token limits
                                qa_chunks = self._chunk_text(chunk)
                                for qa_chunk in qa_chunks:
                                    qa_pairs = self.llm_processor.generate_qa_pairs(qa_chunk, system_prompt)
                                    for pair in qa_pairs:
                                        pair["source"] = file_path.name
                                        qa_f.write(json.dumps(pair) + "\n")

    def _chunk_text(self, text, max_chars=4000):
        """
        Splits text into chunks of approximately max_chars.
        Respects paragraph boundaries where possible.
        """
        chunks = []
        current_chunk = []
        current_length = 0
        paragraphs = text.split('\n\n') # Split by double newline (paragraphs)

        for paragraph in paragraphs:
            # If a single paragraph is huge, we might need to split it further,
            # but for now let's assume paragraphs are reasonable.
            if current_length + len(paragraph) > max_chars:
                if current_chunk:
                    chunks.append("\n\n".join(current_chunk))
                    current_chunk = []
                    current_length = 0

            current_chunk.append(paragraph)
            current_length += len(paragraph) + 2 # +2 for the newline characters

        if current_chunk:
            chunks.append("\n\n".join(current_chunk))

        return chunks

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

            return cleaned_text
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None

# Future placeholders for other types
class AudioDataProcessor(DataProcessor):
    def _process_file(self, file_path):
        # TODO: Implement Whisper or other transcription logic here
        pass
