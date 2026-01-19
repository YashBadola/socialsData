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
        """Syncs the database with the file system."""
        if not self.base_dir.exists():
            return

        # Sync Personalities
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
                    print(f"Error syncing {d.name}: {e}")

    def list_personalities(self):
        """Returns a list of available personality IDs."""
        # Query DB first
        self.db.connect()
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id FROM personalities")
        rows = cursor.fetchall()
        self.db.close()
        # If DB is empty but FS has stuff (shouldn't happen due to sync), fallback
        if not rows:
             return [
                d.name for d in self.base_dir.iterdir()
                if d.is_dir() and (d / "metadata.json").exists()
            ]
        return [row[0] for row in rows]

    def create_personality(self, name):
        """Creates a new personality directory structure and adds to DB."""
        safe_id = name.lower().replace(" ", "_").replace("-", "_")
        target_dir = self.base_dir / safe_id

        if target_dir.exists():
            # If it exists on FS, check if in DB. If not, sync it.
            if not self.db.get_personality(safe_id):
                 self.sync_db()
                 if self.db.get_personality(safe_id):
                     raise FileExistsError(f"Personality '{safe_id}' already exists.")
            else:
                 raise FileExistsError(f"Personality '{safe_id}' already exists.")

        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / "raw").mkdir(exist_ok=True)
        (target_dir / "processed").mkdir(exist_ok=True)

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
        # Prefer DB
        p = self.db.get_personality(personality_id)
        if p:
            # Reconstruct the metadata dict expected by consumers
            path = self.base_dir / personality_id / "metadata.json"
            if path.exists():
                with open(path, "r") as f:
                    meta = json.load(f)
                # Update with DB truth
                meta["name"] = p["name"]
                meta["description"] = p["description"]
                meta["system_prompt"] = p["system_prompt"]
                return meta
            else:
                return {
                    "name": p["name"],
                    "id": p["id"],
                    "description": p["description"],
                    "system_prompt": p["system_prompt"],
                    "sources": [],
                    "license": "Unknown"
                }
        else:
             # Fallback to FS
            path = self.base_dir / personality_id / "metadata.json"
            if not path.exists():
                raise FileNotFoundError(f"Personality '{personality_id}' not found.")
            with open(path, "r") as f:
                return json.load(f)
