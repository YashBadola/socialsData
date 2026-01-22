import sys
import os
from pathlib import Path
import json

from socials_data.core.db import DatabaseManager
from socials_data.core.manager import PersonalityManager

def migrate():
    print("Starting migration to SQLite...")
    db = DatabaseManager()
    manager = PersonalityManager()

    personalities = manager.list_personalities()
    print(f"Found {len(personalities)} personalities to migrate.")

    for pid in personalities:
        print(f"Migrating {pid}...")
        try:
            # 1. Metadata
            meta = manager.get_metadata(pid)
            db.upsert_personality(meta)

            # 2. Processed Data
            # We clear existing data first to ensure clean state
            db.clear_processed_data(pid)

            processed_file = manager.base_dir / pid / "processed" / "data.jsonl"
            if processed_file.exists():
                count = 0
                with open(processed_file, "r") as f:
                    for line in f:
                        try:
                            record = json.loads(line)
                            db.insert_processed_data(pid, record.get("text"), record.get("source"))
                            count += 1
                        except json.JSONDecodeError:
                            print(f"Skipping invalid json line in {pid}/processed/data.jsonl")
                print(f"  Migrated {count} processed chunks.")

            # 3. QA Data
            qa_file = manager.base_dir / pid / "processed" / "qa.jsonl"
            if qa_file.exists():
                qa_count = 0
                with open(qa_file, "r") as f:
                    for line in f:
                        try:
                            record = json.loads(line)
                            db.insert_qa_pair(pid, record.get("source"), record.get("question"), record.get("answer"))
                            qa_count += 1
                        except json.JSONDecodeError:
                             print(f"Skipping invalid json line in {pid}/processed/qa.jsonl")
                print(f"  Migrated {qa_count} QA pairs.")

        except Exception as e:
            print(f"Error migrating {pid}: {e}")

    print("Migration complete.")

if __name__ == "__main__":
    migrate()
