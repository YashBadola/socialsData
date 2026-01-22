import sys
import os
import json
from pathlib import Path

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from socials_data.core.manager import PersonalityManager
from socials_data.core.db import DatabaseManager

def build_db():
    print("Building database...")
    db_manager = DatabaseManager()
    db_manager.connect()
    db_manager.initialize_schema()

    manager = PersonalityManager()
    personalities = manager.list_personalities()

    for p_id in personalities:
        print(f"Processing {p_id}...")
        try:
            metadata = manager.get_metadata(p_id)
            db_manager.add_personality(
                p_id,
                metadata.get("name"),
                metadata.get("description"),
                metadata.get("system_prompt")
            )

            # Process chunks
            data_file = manager.base_dir / p_id / "processed" / "data.jsonl"
            if data_file.exists():
                with open(data_file, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            record = json.loads(line)
                            text = record.get("text")
                            source = record.get("source")
                            if text:
                                db_manager.add_chunk(p_id, text, source)
                        except json.JSONDecodeError:
                            print(f"Skipping invalid JSON line in {data_file}")

            # Process QA pairs
            qa_file = manager.base_dir / p_id / "processed" / "qa.jsonl"
            if qa_file.exists():
                with open(qa_file, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            record = json.loads(line)
                            instruction = record.get("instruction")
                            response = record.get("response")
                            source = record.get("source")

                            if instruction and response:
                                # We pass None for chunk_id because we can't easily link it back
                                # to the specific chunk without more complex logic or data changes.
                                db_manager.add_qa_pair(
                                    instruction,
                                    response,
                                    chunk_id=None,
                                    personality_id=p_id,
                                    source=source
                                )
                        except json.JSONDecodeError:
                            print(f"Skipping invalid JSON line in {qa_file}")

        except Exception as e:
            print(f"Error processing {p_id}: {e}")

    db_manager.close()
    print("Database build complete.")

if __name__ == "__main__":
    build_db()
