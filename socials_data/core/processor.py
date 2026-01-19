import json
from pathlib import Path
import os
import logging
from socials_data.core.llm import LLMProcessor
from socials_data.core.db import Database

class DataProcessor:
    def __init__(self):
        self.llm_processor = LLMProcessor()
        self.db = Database()

    def process(self, personality_dir, skip_qa=False):
        """
        Reads files from raw/, ingests them into DB, processes them into chunks,
        and writes to processed/data.jsonl (for compatibility) and DB.
        If skip_qa is False, it also attempts to generate Q&A pairs.
        """
        personality_dir = Path(personality_dir)
        personality_id = personality_dir.name

        raw_dir = personality_dir / "raw"
        processed_dir = personality_dir / "processed"
        output_file = processed_dir / "data.jsonl"
        qa_output_file = processed_dir / "qa.jsonl"

        # Ensure personality exists in DB
        if not self.db.get_personality(personality_id):
             # Try to load from metadata.json if not in DB
             metadata_file = personality_dir / "metadata.json"
             if metadata_file.exists():
                 with open(metadata_file, "r") as f:
                     meta = json.load(f)
                     try:
                        self.db.add_personality(
                            meta.get("id"),
                            meta.get("name"),
                            meta.get("description", ""),
                            meta.get("system_prompt", ""),
                            meta.get("license", "Unknown")
                        )
                     except ValueError:
                         pass # Already exists

        p_data = self.db.get_personality(personality_id)
        if not p_data:
            print(f"Error: Personality '{personality_id}' not found in DB or metadata.")
            return

        system_prompt = p_data['system_prompt']

        processed_dir.mkdir(parents=True, exist_ok=True)

        # 1. Ingest Raw Files into DB
        if raw_dir.exists():
            for file_path in raw_dir.iterdir():
                if file_path.is_file():
                    # check if already ingested? For now, we trust the DB or we can check.
                    # We'll just read content and see if we can process it.
                    content = self._read_file_content(file_path)
                    if content:
                        # Check if document already exists to avoid duplicates
                        # A simple check by filename
                        docs = self.db.get_documents(personality_id)
                        existing_files = [d['filename'] for d in docs]

                        if file_path.name not in existing_files:
                            print(f"Ingesting {file_path.name} into database...")
                            self.db.add_document(personality_id, file_path.name, content)

        # 2. Process Documents from DB
        documents = self.db.get_documents(personality_id)

        # Prepare JSONL files for backward compatibility
        with open(output_file, "w", encoding="utf-8") as out_f:
             if not skip_qa:
                 qa_f = open(qa_output_file, "w", encoding="utf-8")

             try:
                for doc in documents:
                    doc_id = doc['id']
                    filename = doc['filename']
                    content = doc['content']

                    # Clear existing chunks for this document to avoid duplication on re-run
                    self.db.clear_chunks(doc_id)

                    # Process content (chunking)
                    chunks = self._chunk_text(content)

                    for i, chunk_text in enumerate(chunks):
                        # Add to DB
                        chunk_id = self.db.add_chunk(doc_id, chunk_text, i)

                        # Write to JSONL
                        record = {"text": chunk_text, "source": filename}
                        out_f.write(json.dumps(record) + "\n")

                        # 3. Generate Q&A
                        if not skip_qa and system_prompt and self.llm_processor.client:
                            print(f"Generating Q&A for chunk {i} of {filename}...")
                            qa_pairs = self.llm_processor.generate_qa_pairs(chunk_text, system_prompt)
                            for pair in qa_pairs:
                                # Add to DB
                                self.db.add_qa_pair(chunk_id, pair["instruction"], pair["response"])

                                # Write to JSONL
                                pair["source"] = filename
                                qa_f.write(json.dumps(pair) + "\n")
             finally:
                 if not skip_qa and 'qa_f' in locals():
                     qa_f.close()

    def generate_qa_only(self, personality_dir):
        """
        Generates Q&A pairs from existing chunks in DB.
        """
        personality_dir = Path(personality_dir)
        personality_id = personality_dir.name
        processed_dir = personality_dir / "processed"
        qa_output_file = processed_dir / "qa.jsonl"

        p_data = self.db.get_personality(personality_id)
        if not p_data:
            print("Personality not found.")
            return

        system_prompt = p_data['system_prompt']
        if not system_prompt:
            print("No system prompt found.")
            return

        if not self.llm_processor.client:
            print("No OpenAI API Key found.")
            return

        print(f"Generating Q&A from DB for {personality_id}...")

        # Get all chunks via documents
        # Ideally we should select chunks directly if we had personality_id link, but we go via documents
        documents = self.db.get_documents(personality_id)

        with open(qa_output_file, "w", encoding="utf-8") as qa_f:
            for doc in documents:
                doc_id = doc['id']
                chunks = self.db.get_chunks(doc_id)

                for chunk in chunks:
                    chunk_text = chunk['text']
                    chunk_id = chunk['id']

                    qa_pairs = self.llm_processor.generate_qa_pairs(chunk_text, system_prompt)
                    for pair in qa_pairs:
                        self.db.add_qa_pair(chunk_id, pair["instruction"], pair["response"])
                        pair["source"] = doc['filename']
                        qa_f.write(json.dumps(pair) + "\n")
                        qa_f.flush()

        print(f"Done. Q&A saved to DB and {qa_output_file}")


    def _read_file_content(self, file_path):
        """Reads file content."""
        # Basic extensions check
        if file_path.suffix.lower() not in ['.txt', '.md']:
            return None
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None

    def _chunk_text(self, text):
        """
        Chunks text respecting word boundaries.
        """
        # Basic cleaning: collapse multiple newlines, strip whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        cleaned_text = "\n".join(lines)

        chunk_size = 4000
        chunks = []
        current_chunk = []
        current_length = 0

        words = cleaned_text.split(' ')

        for word in words:
            word_len = len(word) + 1 # +1 for space
            if current_length + word_len > chunk_size:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = []
                    current_length = 0

            current_chunk.append(word)
            current_length += word_len

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

class TextDataProcessor(DataProcessor):
    pass
