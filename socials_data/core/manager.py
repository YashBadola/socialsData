import os
import json
import shutil
from pathlib import Path
from socials_data.core.db import Database

PERSONALITIES_DIR = Path(__file__).parent.parent / "personalities"

class PersonalityManager:
    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir) if base_dir else PERSONALITIES_DIR
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.db = Database()

    def list_personalities(self):
        """Returns a list of available personality IDs."""
        # Get from DB
        db_personalities = [p['id'] for p in self.db.list_personalities()]

        # Get from Filesystem
        if not self.base_dir.exists():
            dir_personalities = []
        else:
            dir_personalities = [
                d.name for d in self.base_dir.iterdir()
                if d.is_dir() and (d / "metadata.json").exists()
            ]

        # Merge unique
        return sorted(list(set(db_personalities + dir_personalities)))

    def create_personality(self, name):
        """Creates a new personality directory structure and adds to DB."""
        safe_id = name.lower().replace(" ", "_").replace("-", "_")
        target_dir = self.base_dir / safe_id

        # Check existence in both DB and FS
        in_db = self.db.get_personality(safe_id) is not None
        in_fs = target_dir.exists()

        if in_db and in_fs:
            raise FileExistsError(f"Personality '{safe_id}' already exists.")

        if not target_dir.exists():
            target_dir.mkdir()
            (target_dir / "raw").mkdir()
            (target_dir / "processed").mkdir()

        metadata = {
            "name": name,
            "id": safe_id,
            "description": "",
            "system_prompt": "",
            "sources": [],
            "license": "Unknown"
        }

        # Write to file (legacy/backup)
        with open(target_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        # Add to DB
        self.db.add_personality(safe_id, name, "", "", "Unknown")

        return safe_id

    def get_metadata(self, personality_id):
        # Try DB first
        p = self.db.get_personality(personality_id)
        if p:
            sources = []
            documents = self.db.get_documents(personality_id)
            for doc in documents:
                # doc structure: (id, personality_id, filename, content, source_url, type)
                sources.append({
                    "title": doc[2],
                    "url": doc[4] if doc[4] else "",
                    "type": doc[5]
                })

            return {
                "name": p["name"],
                "id": p["id"],
                "description": p["description"],
                "system_prompt": p["system_prompt"],
                "license": p["license"],
                "sources": sources
            }

        # Fallback to file
        path = self.base_dir / personality_id / "metadata.json"
        if not path.exists():
            raise FileNotFoundError(f"Personality '{personality_id}' not found.")
        with open(path, "r") as f:
            return json.load(f)
