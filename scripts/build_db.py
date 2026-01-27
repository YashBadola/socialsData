import json
import os
from pathlib import Path
from socials_data.db.manager import DatabaseManager

def main():
    manager = DatabaseManager()
    base_dir = Path("socials_data/personalities")

    print("Building database...")

    for personality_dir in base_dir.iterdir():
        if not personality_dir.is_dir():
            continue

        p_id = personality_dir.name
        metadata_file = personality_dir / "metadata.json"

        if not metadata_file.exists():
            print(f"Skipping {p_id}: No metadata.json")
            continue

        try:
            with open(metadata_file, "r") as f:
                meta = json.load(f)

            name = meta.get("name", p_id)
            description = meta.get("description", "")
            system_prompt = meta.get("system_prompt", "")

            manager.add_personality(p_id, name, description, system_prompt)
            print(f"Added personality: {name}")

            # Add Works (Sources)
            sources = meta.get("sources", [])
            for src in sources:
                title = src.get("title", "Unknown")
                url = src.get("url")
                manager.add_work(p_id, title, url)

            # Add Segments
            data_file = personality_dir / "processed" / "data.jsonl"
            if data_file.exists():
                count = 0
                with open(data_file, "r", encoding="utf-8") as f:
                    for i, line in enumerate(f):
                        try:
                            record = json.loads(line)
                            content = record.get("text")
                            source_file = record.get("source", "")

                            # Try to find matching work ID based on source file name
                            work_id = None
                            clean_source = source_file.lower().replace("_", " ").replace(".txt", "")

                            matched_work_title = None
                            for src in sources:
                                t = src.get("title", "").lower()
                                if t and t in clean_source:
                                    matched_work_title = src.get("title")
                                    break

                            if matched_work_title:
                                work_id = manager.add_work(p_id, matched_work_title)

                            segment_id = manager.add_segment(p_id, content, work_id=work_id, sequence_index=i)
                            count += 1
                        except json.JSONDecodeError:
                            continue
                print(f"  Added {count} segments.")

            else:
                print(f"  No data.jsonl found.")

        except Exception as e:
            print(f"Error processing {p_id}: {e}")

    stats = manager.get_stats()
    print("\nDatabase Statistics:")
    print(json.dumps(stats, indent=2))
    print(f"\nDatabase saved to {manager.db_path}")

if __name__ == "__main__":
    main()
