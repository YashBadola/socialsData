import json
from pathlib import Path
import os
import logging
from socials_data.core.llm import LLMProcessor

class DataProcessor:
    def __init__(self):
        self.llm_processor = LLMProcessor()

    def process(self, personality_dir, skip_qa=False):
        """
        Reads files from raw/, processes them, and writes to processed/data.jsonl.
        If skip_qa is False, it also attempts to generate Q&A pairs.
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
        with open(output_file, "w", encoding="utf-8") as out_f:
             # If not skipping QA, we open QA file too, initially empty or appending?
             # To keep it simple, we overwrite both if running full process.
             if not skip_qa:
                 qa_f = open(qa_output_file, "w", encoding="utf-8")

             try:
                for file_path in raw_dir.iterdir():
                    if file_path.is_file():
                        content = self._process_file(file_path)
                        if content:
                            # 1. Write standard text data
                            chunks = content if isinstance(content, list) else [content]

                            for chunk in chunks:
                                record = {"text": chunk, "source": file_path.name}
                                out_f.write(json.dumps(record) + "\n")

                                # 2. If we have a system prompt and valid text, generate Q&A
                                if not skip_qa and system_prompt and self.llm_processor.client:
                                    print(f"Generating Q&A for {file_path.name}...") # User feedback
                                    qa_pairs = self.llm_processor.generate_qa_pairs(chunk, system_prompt)
                                    for pair in qa_pairs:
                                        pair["source"] = file_path.name
                                        qa_f.write(json.dumps(pair) + "\n")
             finally:
                 if not skip_qa and 'qa_f' in locals():
                     qa_f.close()

    def generate_qa_only(self, personality_dir):
        """
        Generates Q&A pairs from existing processed/data.jsonl.
        Useful if one wants to run QA generation separately or re-run it.
        """
        personality_dir = Path(personality_dir)
        processed_dir = personality_dir / "processed"
        input_file = processed_dir / "data.jsonl"
        qa_output_file = processed_dir / "qa.jsonl"

        if not input_file.exists():
            print(f"Error: {input_file} does not exist. Run 'process' first.")
            return

        metadata_file = personality_dir / "metadata.json"
        system_prompt = None
        if metadata_file.exists():
            try:
                with open(metadata_file, "r") as f:
                    meta = json.load(f)
                    system_prompt = meta.get("system_prompt")
            except Exception as e:
                logging.error(f"Failed to read metadata: {e}")
                return

        if not system_prompt:
            print("No 'system_prompt' found in metadata. Cannot generate Q&A.")
            return

        if not self.llm_processor.client:
            print("No OpenAI API Key found. Cannot generate Q&A.")
            return

        print(f"Generating Q&A from existing data for {personality_dir.name}...")

        with open(input_file, "r", encoding="utf-8") as in_f, \
             open(qa_output_file, "w", encoding="utf-8") as qa_f:

            for line in in_f:
                try:
                    record = json.loads(line)
                    chunk = record.get("text")
                    source = record.get("source", "unknown")

                    if chunk:
                        qa_pairs = self.llm_processor.generate_qa_pairs(chunk, system_prompt)
                        for pair in qa_pairs:
                            pair["source"] = source
                            qa_f.write(json.dumps(pair) + "\n")
                            # flush to see progress?
                            qa_f.flush()
                except json.JSONDecodeError:
                    continue

        print(f"Done. Q&A saved to {qa_output_file}")


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
            # But preserve paragraph structure (double newlines)
            cleaned_text = text.replace('\r\n', '\n')
            # Replace 3 or more newlines with 2
            while '\n\n\n' in cleaned_text:
                cleaned_text = cleaned_text.replace('\n\n\n', '\n\n')

            # Simple chunking if text is too large could be added here
            # For now, we return the whole cleaned text as one chunk
            # Breaking into chunks of roughly 2000 chars to enable better dataset handling
            chunks = []
            current_chunk = []
            current_len = 0

            for paragraph in cleaned_text.split('\n\n'):
                # restore paragraphs with double newlines
                if not paragraph.strip():
                    continue

                p_len = len(paragraph)
                if current_len + p_len > 2000:
                    if current_chunk:
                        chunks.append("\n\n".join(current_chunk))
                    current_chunk = [paragraph]
                    current_len = p_len
                else:
                    current_chunk.append(paragraph)
                    current_len += p_len + 2 # +2 for the newlines

            if current_chunk:
                chunks.append("\n\n".join(current_chunk))

            return chunks
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None

# Future placeholders for other types
class AudioDataProcessor(DataProcessor):
    def _process_file(self, file_path):
        # TODO: Implement Whisper or other transcription logic here
        pass
