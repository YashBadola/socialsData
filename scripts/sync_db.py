import json
from pathlib import Path
from socials_data.core.manager import PersonalityManager
from socials_data.core.db import SocialsDatabase

def sync_db():
    manager = PersonalityManager()
    db = SocialsDatabase()

    personalities = manager.list_personalities()
    print(f"Found {len(personalities)} personalities.")

    for p_id in personalities:
        print(f"Syncing {p_id}...")
        try:
            # 1. Sync Metadata
            metadata = manager.get_metadata(p_id)
            db.upsert_personality(metadata)

            # 2. Sync Content
            processed_file = manager.base_dir / p_id / "processed" / "data.jsonl"
            chunks = []
            if processed_file.exists():
                with open(processed_file, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            record = json.loads(line)
                            chunks.append(record)
                        except json.JSONDecodeError:
                            continue

                db.index_chunks(p_id, chunks)
                print(f"  Indexed {len(chunks)} chunks.")
            else:
                print("  No processed data found.")

        except Exception as e:
            print(f"  Error syncing {p_id}: {e}")

    print("Sync complete.")

if __name__ == "__main__":
    sync_db()
