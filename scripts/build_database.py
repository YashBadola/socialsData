import os
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from socials_data.core.db import DatabaseManager
from socials_data.core.processor import TextDataProcessor

PERSONALITIES_DIR = Path("socials_data/personalities")

def build_database():
    db = DatabaseManager()
    processor = TextDataProcessor()

    print("Building database...")

    for personality_dir in PERSONALITIES_DIR.iterdir():
        if not personality_dir.is_dir():
            continue

        metadata_path = personality_dir / "metadata.json"
        if not metadata_path.exists():
            print(f"Skipping {personality_dir.name}: No metadata.json")
            continue

        print(f"Processing {personality_dir.name}...")

        # Load metadata
        with open(metadata_path, "r") as f:
            metadata = json.load(f)

        pid = metadata.get("id", personality_dir.name)

        # Add personality
        db.add_personality(
            id=pid,
            name=metadata.get("name", "Unknown"),
            description=metadata.get("description", ""),
            system_prompt=metadata.get("system_prompt", ""),
            license=metadata.get("license", "Unknown")
        )

        # Add sources
        for source in metadata.get("sources", []):
            db.add_source(
                personality_id=pid,
                type=source.get("type", "unknown"),
                title=source.get("title", "Unknown"),
                url=source.get("url", "")
            )

        # Add content (Chunks)
        processed_file = personality_dir / "processed" / "data.jsonl"

        # If processed file exists, use it
        if processed_file.exists():
            print(f"  Loading from processed data...")
            with open(processed_file, "r") as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        text = record.get("text")
                        source_name = record.get("source", "unknown")
                        if text:
                            db.add_chunk(pid, source_name, text)
                    except json.JSONDecodeError:
                        continue
        else:
            # If no processed file, try to process raw files on the fly
            print(f"  No processed data found. Processing raw files...")
            raw_dir = personality_dir / "raw"
            if raw_dir.exists():
                for raw_file in raw_dir.iterdir():
                    if raw_file.is_file():
                        content = processor._process_file(raw_file)
                        if content:
                            db.add_chunk(pid, raw_file.name, content)
            else:
                print(f"  No raw directory found for {pid}")

    db.close()
    print("Database build complete.")

if __name__ == "__main__":
    build_database()
