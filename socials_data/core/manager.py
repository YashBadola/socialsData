import os
import json
import shutil
from pathlib import Path
from socials_data.core.db import DBManager

PERSONALITIES_DIR = Path(__file__).parent.parent / "personalities"

class PersonalityManager:
    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir) if base_dir else PERSONALITIES_DIR
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.db = DBManager()
        self.sync_db()

    def sync_db(self):
        """Syncs filesystem personalities to the database."""
        if not self.base_dir.exists():
            return

        for d in self.base_dir.iterdir():
            if d.is_dir() and (d / "metadata.json").exists():
                p_id = d.name
                # Check if exists in DB
                if not self.db.get_personality(p_id):
                    try:
                        with open(d / "metadata.json", "r") as f:
                            meta = json.load(f)
                            self.db.add_personality(
                                p_id=meta.get("id", p_id),
                                name=meta.get("name", p_id),
                                description=meta.get("description", ""),
                                system_prompt=meta.get("system_prompt", ""),
                                license=meta.get("license", "")
                            )
                    except Exception as e:
                        print(f"Error syncing {p_id}: {e}")

    def list_personalities(self):
        """Returns a list of available personality IDs."""
        return self.db.list_personalities()

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
            "sources": [],
            "license": "Unknown"
        }

        with open(target_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        self.db.add_personality(safe_id, name)

        return safe_id

    def get_metadata(self, personality_id):
        # Try DB first
        p = self.db.get_personality(personality_id)
        if p:
            # Reconstruct metadata dict structure roughly
            # Note: sources are not yet in DB personalities table, but sources are usually documents.
            # For compatibility, we might still read the file if we want the full exact structure including sources list if it's there.
            # But the task is to use the new database.
            # Let's rely on the file for the full metadata if available, as DB might be a subset or different structure.
            # But wait, the goal is to develop a NEW database.
            pass

        path = self.base_dir / personality_id / "metadata.json"
        if not path.exists():
             # If in DB but not on disk (unlikely with current logic but possible), return DB version
             if p:
                 return p
             raise FileNotFoundError(f"Personality '{personality_id}' not found.")

        with open(path, "r") as f:
            return json.load(f)
