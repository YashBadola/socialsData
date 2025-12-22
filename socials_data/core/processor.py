import json
from pathlib import Path
import os
import re

class DataProcessor:
    def __init__(self, personality_dir):
        self.p_dir = Path(personality_dir)
        self.raw_dir = self.p_dir / "raw"
        self.processed_dir = self.p_dir / "processed"
        self.processed_dir.mkdir(exist_ok=True)

    def process_text(self):
        # Basic processing: read all txt files in raw, chunk them, and save to data.jsonl
        data = []
        for file in self.raw_dir.glob("*.txt"):
            with open(file, "r", encoding="utf-8") as f:
                text = f.read()

            chunks = self._chunk_text(text)
            for chunk in chunks:
                if chunk.strip(): # Only add non-empty chunks
                    data.append({
                        "text": chunk,
                        "source": file.name
                    })

        with open(self.processed_dir / "data.jsonl", "w") as f:
            for entry in data:
                f.write(json.dumps(entry) + "\n")

    def _chunk_text(self, text, max_chunk_size=1000):
        # Chunk text respecting word boundaries
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0

        for word in words:
            # +1 for the space we'll add back
            if current_length + len(word) + 1 > max_chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)
                current_length += len(word) + 1

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def generate_qa(self):
        # Placeholder for QA generation
        pass
