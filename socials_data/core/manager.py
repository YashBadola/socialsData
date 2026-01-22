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
        self.sync_db()

    def sync_db(self):
        """Syncs filesystem personalities to the database."""
        if not self.base_dir.exists():
            return

        for d in self.base_dir.iterdir():
            if d.is_dir() and (d / "metadata.json").exists():
                try:
                    with open(d / "metadata.json", "r") as f:
                        meta = json.load(f)
                    self.db.add_personality(
                        meta.get("id", d.name),
                        meta.get("name", d.name),
                        meta.get("description", ""),
                        meta.get("system_prompt", "")
                    )
                except Exception as e:
                    print(f"Failed to sync {d.name}: {e}")

    def list_personalities(self):
        """Returns a list of available personality IDs."""
        if not self.base_dir.exists():
            return []
        # Return sorted list of directories that are valid personalities
        return sorted([
            d.name for d in self.base_dir.iterdir()
            if d.is_dir() and (d / "metadata.json").exists()
        ])

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

        self.db.add_personality(safe_id, name, "", "")

        return safe_id

    def get_metadata(self, personality_id):
        # Try DB first
        p = self.db.get_personality(personality_id)
        if p:
             # We might want to merge with file info if needed,
             # but for now let's assume DB has basic info.
             # However, 'sources' and 'license' are not in DB table currently.
             # So we still read the file for full metadata, but use DB to confirm existence.
             pass

        path = self.base_dir / personality_id / "metadata.json"
        if not path.exists():
            raise FileNotFoundError(f"Personality '{personality_id}' not found.")
        with open(path, "r") as f:
            return json.load(f)
