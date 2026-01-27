import json
from pathlib import Path
import os
import logging
import sqlite3
from socials_data.core.llm import LLMProcessor

class DataProcessor:
    def __init__(self):
        self.llm_processor = LLMProcessor()

    def process(self, personality_dir, skip_qa=False):
        """
        Reads files from raw/, processes them, and writes to processed/data.jsonl.
        If skip_qa is False, it also attempts to generate Q&A pairs.
        Also exports data to a SQLite database.
        """
        personality_dir = Path(personality_dir)
        raw_dir = personality_dir / "raw"
        processed_dir = personality_dir / "processed"
        output_file = processed_dir / "data.jsonl"
        qa_output_file = processed_dir / "qa.jsonl"
        db_output_file = processed_dir / "knowledge.db"

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

        all_records = []

        # Prepare files
        # We overwrite to ensure clean state.
        with open(output_file, "w", encoding="utf-8") as out_f:
             # If not skipping QA, we open QA file too, initially empty or appending?
             # To keep it simple, we overwrite both if running full process.
             if not skip_qa:
                 qa_f = open(qa_output_file, "w", encoding="utf-8")

             try:
                if raw_dir.exists():
                    for file_path in raw_dir.iterdir():
                        if file_path.is_file():
                            content = self._process_file(file_path)
                            if content:
                                # 1. Write standard text data
                                chunks = content if isinstance(content, list) else [content]

                                for chunk in chunks:
                                    # Normalize to record dict
                                    if isinstance(chunk, dict):
                                        record = chunk
                                        if "source" not in record:
                                            record["source"] = file_path.name
                                    else:
                                        record = {"text": chunk, "source": file_path.name}

                                    all_records.append(record)
                                    out_f.write(json.dumps(record) + "\n")

                                    # 2. If we have a system prompt and valid text, generate Q&A
                                    # Use 'text' field for Q&A generation
                                    text_for_qa = record.get("text", "")
                                    if not skip_qa and system_prompt and self.llm_processor.client and text_for_qa:
                                        print(f"Generating Q&A for {file_path.name}...") # User feedback
                                        qa_pairs = self.llm_processor.generate_qa_pairs(text_for_qa, system_prompt)
                                        for pair in qa_pairs:
                                            pair["source"] = file_path.name
                                            qa_f.write(json.dumps(pair) + "\n")
             finally:
                 if not skip_qa and 'qa_f' in locals():
                     qa_f.close()

        # 3. Export to SQLite
        if all_records:
            self._export_to_sqlite(all_records, db_output_file)

    def _export_to_sqlite(self, records, db_path):
        """Exports records to a SQLite database."""
        try:
            # Remove existing db to start fresh
            if db_path.exists():
                db_path.unlink()

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Determine columns dynamically from all records
            all_keys = set()
            for r in records:
                all_keys.update(r.keys())

            # Ensure 'id' is primary key if not present (we'll use rowid or auto inc if needed, but let's keep it simple)
            columns = sorted(list(all_keys))
            # Create table
            # We treat everything as TEXT for simplicity, or try to infer types?
            # SQLite is flexible. TEXT is safe.
            cols_def = ", ".join([f'"{col}" TEXT' for col in columns])
            create_query = f"CREATE TABLE knowledge ({cols_def})"
            cursor.execute(create_query)

            # Insert data
            for r in records:
                # Prepare values matching columns order
                values = [str(r.get(col, "")) for col in columns]
                placeholders = ", ".join(["?" for _ in columns])
                # Quote column names to avoid reserved keyword conflicts
                quoted_columns = [f'"{col}"' for col in columns]
                insert_query = f"INSERT INTO knowledge ({', '.join(quoted_columns)}) VALUES ({placeholders})"
                cursor.execute(insert_query, values)

            conn.commit()
            conn.close()
            print(f"Exported {len(records)} records to {db_path}")
        except Exception as e:
            print(f"Error exporting to SQLite: {e}")

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
        Handles text files and json files.
        For text/md: Returns the content as a string.
        For json: Returns the content as a list of dicts or a dict.
        """
        suffix = file_path.suffix.lower()

        # JSON handling
        if suffix == '.json':
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return data
            except Exception as e:
                print(f"Error processing JSON {file_path}: {e}")
                return None

        # Text/MD handling
        if suffix not in ['.txt', '.md']:
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
