from socials_data.core.manager import PersonalityManager
from socials_data.core.db import DatabaseManager
from pathlib import Path
import json
import sys

# Ensure we can import from root
sys.path.append(str(Path(__file__).parent.parent))

def main():
    manager = PersonalityManager()
    db = DatabaseManager()

    personalities = manager.list_personalities()
    print(f"Found {len(personalities)} personalities.")

    for pid in personalities:
        print(f"Processing {pid}...")
        try:
            # Load metadata
            metadata = manager.get_metadata(pid)

            # Insert Personality
            db.add_personality(
                id=pid,
                name=metadata.get("name", pid),
                description=metadata.get("description", ""),
                system_prompt=metadata.get("system_prompt", "")
            )

            # Insert Works (Sources)
            sources = metadata.get("sources", [])
            for source in sources:
                db.add_work(
                    personality_id=pid,
                    title=source.get("title", "Unknown"),
                    type=source.get("type", "unknown"),
                    url=source.get("url")
                )

            # Insert Excerpts from RAW files
            # Note: We are reading raw files directly.
            # In a more advanced version, we might process them first or link them to specific works.
            personality_dir = manager.base_dir / pid
            raw_dir = personality_dir / "raw"

            if raw_dir.exists():
                for file_path in raw_dir.iterdir():
                    if file_path.is_file() and file_path.suffix in ['.txt', '.md']:
                        with open(file_path, "r", encoding="utf-8") as f:
                            text = f.read()
                            # Here we just insert the whole file content or split by lines?
                            # Let's split by empty lines to get "paragraphs" or "aphorisms"
                            chunks = [c.strip() for c in text.split('\n\n') if c.strip()]

                            for chunk in chunks:
                                db.add_excerpt(
                                    personality_id=pid,
                                    text=chunk,
                                    source_file=file_path.name
                                )
        except Exception as e:
            print(f"Error processing {pid}: {e}")

    print("Database population complete.")

if __name__ == "__main__":
    main()
