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
        self.db.init_db()

    def list_personalities(self):
        """Returns a list of available personality IDs from the database."""
        # We can also fall back to directories if DB is empty?
        # For now, let's just list directories as that is the source of truth for content
        if not self.base_dir.exists():
            return []
        return [
            d.name for d in self.base_dir.iterdir()
            if d.is_dir() and (d / "metadata.json").exists()
        ]

    def create_personality(self, name):
        """Creates a new personality directory structure and adds to DB."""
        safe_id = name.lower().replace(" ", "_").replace("-", "_")
        target_dir = self.base_dir / safe_id

        if target_dir.exists():
            raise FileExistsError(f"Personality '{safe_id}' already exists.")

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

        with open(target_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        # Add to DB
        self.db.add_personality(safe_id, name, "", "")

        return safe_id

    def get_metadata(self, personality_id):
        # Try DB first
        p = self.db.get_personality(personality_id)
        if p:
             # Basic metadata
             # But sources list is in the JSON file.
             # For now let's read from file to be safe as it contains the full structure
             pass

        path = self.base_dir / personality_id / "metadata.json"
        if not path.exists():
            raise FileNotFoundError(f"Personality '{personality_id}' not found.")
        with open(path, "r") as f:
            return json.load(f)

    def sync_db(self):
        """Syncs filesystem metadata to the database."""
        for p_id in self.list_personalities():
            meta = self.get_metadata(p_id)
            self.db.add_personality(
                p_id,
                meta.get("name"),
                meta.get("description"),
                meta.get("system_prompt")
            )
