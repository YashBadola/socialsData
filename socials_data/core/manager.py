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
        """Returns a list of available personality IDs from the DB."""
        return self.db.list_personalities()

    def create_personality(self, name):
        """Creates a new personality in DB and directory structure."""
        safe_id = name.lower().replace(" ", "_").replace("-", "_")
        target_dir = self.base_dir / safe_id

        # We create the directory for raw files still, as we might want to drop files there manually
        if not target_dir.exists():
            target_dir.mkdir(parents=True, exist_ok=True)
            (target_dir / "raw").mkdir(exist_ok=True)
            (target_dir / "processed").mkdir(exist_ok=True)

        metadata = {
            "name": name,
            "id": safe_id,
            "description": "",
            "sources": [],
            "license": "Unknown"
        }

        # Add to DB
        self.db.add_personality(safe_id, name, "", "", metadata)

        # Also write metadata.json for backward compatibility or easy editing
        with open(target_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        return safe_id

    def get_metadata(self, personality_id):
        # Try DB first
        p = self.db.get_personality(personality_id)
        if p:
            # Construct metadata dict similar to what was in json
            meta = p['metadata']
            meta['name'] = p['name']
            meta['id'] = p['id']
            meta['description'] = p['description']
            meta['system_prompt'] = p['system_prompt']
            return meta

        # Fallback to file system
        path = self.base_dir / personality_id / "metadata.json"
        if not path.exists():
            raise FileNotFoundError(f"Personality '{personality_id}' not found.")
        with open(path, "r") as f:
            return json.load(f)

    def migrate_from_files(self):
        """Migrates existing personalities from file system to DB."""
        if not self.base_dir.exists():
            return

        for d in self.base_dir.iterdir():
            if d.is_dir() and (d / "metadata.json").exists():
                try:
                    with open(d / "metadata.json", "r") as f:
                        meta = json.load(f)

                    p_id = meta.get("id", d.name)
                    name = meta.get("name", p_id)
                    description = meta.get("description", "")
                    system_prompt = meta.get("system_prompt", "")

                    self.db.add_personality(p_id, name, description, system_prompt, meta)
                    print(f"Migrated {p_id} to database.")
                except Exception as e:
                    print(f"Error migrating {d.name}: {e}")
