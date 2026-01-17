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
        Reads files from raw/, processes them, and writes to processed/data.jsonl and the Database.
        If skip_qa is False, it also attempts to generate Q&A pairs.
        """
        personality_dir = Path(personality_dir)
        personality_id = personality_dir.name
        raw_dir = personality_dir / "raw"
        processed_dir = personality_dir / "processed"
        output_file = processed_dir / "data.jsonl"
        qa_output_file = processed_dir / "qa.jsonl"

        # Get system prompt from DB or file
        system_prompt = None
        p_data = self.db.get_personality(personality_id)
        if p_data:
            system_prompt = p_data.get("system_prompt")
        else:
            metadata_file = personality_dir / "metadata.json"
            if metadata_file.exists():
                try:
                    with open(metadata_file, "r") as f:
                        meta = json.load(f)
                        system_prompt = meta.get("system_prompt")
                except Exception as e:
                    logging.error(f"Failed to read metadata: {e}")

        processed_dir.mkdir(parents=True, exist_ok=True)

        # Clear existing data in DB for this personality to avoid dupes
        self.db.clear_personality_data(personality_id)

        # Prepare files
        with open(output_file, "w", encoding="utf-8") as out_f:
             if not skip_qa:
                 qa_f = open(qa_output_file, "w", encoding="utf-8")

             try:
                for file_path in raw_dir.iterdir():
                    if file_path.is_file():
                        content = self._process_file(file_path)
                        if content:
                            chunks = content if isinstance(content, list) else [content]

                            # Add document to DB
                            full_text = "\n".join(chunks)
                            doc_id = self.db.add_document(personality_id, file_path.name, full_text, source_url=None)

                            for i, chunk in enumerate(chunks):
                                # DB: Add Chunk
                                chunk_id = self.db.add_chunk(doc_id, chunk, i)

                                # File: Write standard text data
                                record = {"text": chunk, "source": file_path.name}
                                out_f.write(json.dumps(record) + "\n")

                                # 2. If we have a system prompt and valid text, generate Q&A
                                if not skip_qa and system_prompt and self.llm_processor.client:
                                    print(f"Generating Q&A for {file_path.name}...")
                                    qa_pairs = self.llm_processor.generate_qa_pairs(chunk, system_prompt)
                                    for pair in qa_pairs:
                                        pair["source"] = file_path.name
                                        # File: Write QA
                                        qa_f.write(json.dumps(pair) + "\n")
                                        # DB: Add QA
                                        self.db.add_qa_pair(
                                            personality_id,
                                            pair.get("instruction", ""),
                                            pair.get("response", ""),
                                            file_path.name,
                                            chunk_id
                                        )
             finally:
                 if not skip_qa and 'qa_f' in locals():
                     qa_f.close()

    def generate_qa_only(self, personality_dir):
        """
        Generates Q&A pairs from DB chunks (or file if DB empty? No, assume DB populated).
        """
        personality_dir = Path(personality_dir)
        personality_id = personality_dir.name

        # Get chunks from DB
        documents = self.db.get_documents(personality_id)
        if not documents:
             print(f"No documents found in DB for {personality_id}. Run 'process' first.")
             return

        system_prompt = None
        p_data = self.db.get_personality(personality_id)
        if p_data:
            system_prompt = p_data.get("system_prompt")

        if not system_prompt:
            print("No 'system_prompt' found. Cannot generate Q&A.")
            return

        if not self.llm_processor.client:
            print("No OpenAI API Key found. Cannot generate Q&A.")
            return

        print(f"Generating Q&A from DB data for {personality_dir.name}...")

        conn = self.db.get_connection()
        cursor = conn.cursor()

        qa_output_file = personality_dir / "processed" / "qa.jsonl"

        with open(qa_output_file, "w", encoding="utf-8") as qa_f:
            for doc in documents:
                doc_id = doc['id']
                cursor.execute('SELECT * FROM chunks WHERE document_id = ? ORDER BY chunk_index', (doc_id,))
                chunks = [dict(row) for row in cursor.fetchall()]

                for chunk_row in chunks:
                    chunk_text = chunk_row['text']
                    chunk_id = chunk_row['id']
                    source = doc['filename']

                    if chunk_text:
                        qa_pairs = self.llm_processor.generate_qa_pairs(chunk_text, system_prompt)
                        for pair in qa_pairs:
                            pair["source"] = source
                            # File
                            qa_f.write(json.dumps(pair) + "\n")
                            qa_f.flush()
                            # DB
                            self.db.add_qa_pair(
                                personality_id,
                                pair.get("instruction", ""),
                                pair.get("response", ""),
                                source,
                                chunk_id
                            )

        print(f"Done. Q&A saved to DB and {qa_output_file}")


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
