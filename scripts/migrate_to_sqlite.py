import os
import json
import logging
from pathlib import Path
from socials_data.core.db import init_db, add_personality, add_chunk, add_qa_pair

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PERSONALITIES_DIR = Path("socials_data/personalities")
DB_PATH = Path("philosophers.db")

def migrate():
    logger.info("Initializing database...")
    init_db(DB_PATH)

    if not PERSONALITIES_DIR.exists():
        logger.error(f"Personalities directory not found: {PERSONALITIES_DIR}")
        return

    for personality_dir in PERSONALITIES_DIR.iterdir():
        if not personality_dir.is_dir():
            continue

        metadata_path = personality_dir / "metadata.json"
        if not metadata_path.exists():
            logger.warning(f"Skipping {personality_dir.name}: No metadata.json")
            continue

        # 1. Add Personality
        try:
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
            logger.info(f"Migrating {metadata['name']} ({metadata['id']})...")
            add_personality(DB_PATH, metadata)
        except Exception as e:
            logger.error(f"Error loading metadata for {personality_dir.name}: {e}")
            continue

        personality_id = metadata["id"]

        # 2. Add Chunks
        data_path = personality_dir / "processed" / "data.jsonl"
        if data_path.exists():
            try:
                with open(data_path, "r") as f:
                    for line in f:
                        try:
                            record = json.loads(line)
                            add_chunk(
                                DB_PATH,
                                personality_id,
                                record.get("source", "unknown"),
                                record.get("text", "")
                            )
                        except json.JSONDecodeError:
                            continue
                logger.info(f"  Added chunks for {personality_id}")
            except Exception as e:
                logger.error(f"Error migrating chunks for {personality_id}: {e}")

        # 3. Add QA Pairs
        qa_path = personality_dir / "processed" / "qa.jsonl"
        if qa_path.exists():
            try:
                with open(qa_path, "r") as f:
                    for line in f:
                        try:
                            record = json.loads(line)
                            add_qa_pair(
                                DB_PATH,
                                personality_id,
                                None, # chunk_id unknown for existing data
                                record.get("instruction", ""),
                                record.get("response", ""),
                                record.get("source", "unknown")
                            )
                        except json.JSONDecodeError:
                            continue
                logger.info(f"  Added QA pairs for {personality_id}")
            except Exception as e:
                logger.error(f"Error migrating QA for {personality_id}: {e}")

    logger.info("Migration complete.")

if __name__ == "__main__":
    migrate()
