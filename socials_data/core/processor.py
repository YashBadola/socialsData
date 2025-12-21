import json
from pathlib import Path
import os

class DataProcessor:
    def process(self, personality_dir):
        """
        Reads files from raw/, processes them, and writes to processed/data.jsonl.
        """
        personality_dir = Path(personality_dir)
        raw_dir = personality_dir / "raw"
        processed_dir = personality_dir / "processed"
        output_file = processed_dir / "data.jsonl"

        processed_dir.mkdir(parents=True, exist_ok=True)

        # Open in append mode or write mode?
        # For simplicity in this template, we overwrite to ensure clean state.
        with open(output_file, "w", encoding="utf-8") as out_f:
            for file_path in raw_dir.iterdir():
                if file_path.is_file():
                    content = self._process_file(file_path)
                    if content:
                        # We allow _process_file to return a list of text chunks or a single string
                        if isinstance(content, list):
                            for chunk in content:
                                record = {"text": chunk, "source": file_path.name}
                                out_f.write(json.dumps(record) + "\n")
                        else:
                            record = {"text": content, "source": file_path.name}
                            out_f.write(json.dumps(record) + "\n")

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
