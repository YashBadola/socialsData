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
        if not self.base_dir.exists():
            return []
        return [
            d.name for d in self.base_dir.iterdir()
            if d.is_dir() and (d / "metadata.json").exists()
        ]

    def create_personality(self, name):
        """Creates a new personality directory structure."""
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
        path = self.base_dir / personality_id / "metadata.json"
        if not path.exists():
            # Try DB
            p_data = self.db.get_personality(personality_id)
            if p_data:
                return p_data
            raise FileNotFoundError(f"Personality '{personality_id}' not found.")

        with open(path, "r") as f:
            data = json.load(f)

        return data

    def register_personality(self, personality_id):
        """Ensures the personality exists in the DB."""
        data = self.get_metadata(personality_id)
        self.db.add_personality(
            data.get("id", personality_id),
            data.get("name", ""),
            data.get("description", ""),
            data.get("system_prompt", "")
        )

    def sync_to_db(self, personality_id):
        """Syncs a personality's metadata and raw files to the DB."""
        self.register_personality(personality_id)

        # Add sources from raw directory
        raw_dir = self.base_dir / personality_id / "raw"
        if raw_dir.exists():
            for file_path in raw_dir.iterdir():
                if file_path.is_file():
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        self.db.add_source(personality_id, file_path.name, content)
