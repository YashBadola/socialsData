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
        """Returns a list of available personality IDs."""
        # Check filesystem
        if not self.base_dir.exists():
            return []

        fs_personalities = [
            d.name for d in self.base_dir.iterdir()
            if d.is_dir() and (d / "metadata.json").exists()
        ]

        # We could also check DB, but FS is the ground truth for existence of folders
        return fs_personalities

    def create_personality(self, name):
        """Creates a new personality directory structure and DB entry."""
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
            # Reconstruct metadata dict structure roughly
            # Note: DB schema is flat, metadata.json is nested (sources).
            # Ideally we should store sources in DB too, but for now we mix.
            # Let's read file to get full structure, but use DB for core fields if needed.
            pass

        path = self.base_dir / personality_id / "metadata.json"
        if not path.exists():
            raise FileNotFoundError(f"Personality '{personality_id}' not found.")

        with open(path, "r") as f:
            data = json.load(f)

        # Sync to DB if not present or updated
        # This acts as a lazy sync
        self.db.add_personality(
            data.get("id", personality_id),
            data.get("name", ""),
            data.get("description", ""),
            data.get("system_prompt", "")
        )
        return data

    def sync_personality(self, personality_id):
        """Explicitly syncs filesystem data to DB for a personality."""
        data = self.get_metadata(personality_id)
        # add_personality is idempotent (INSERT OR REPLACE)
        self.db.add_personality(
            data.get("id", personality_id),
            data.get("name", ""),
            data.get("description", ""),
            data.get("system_prompt", "")
        )
