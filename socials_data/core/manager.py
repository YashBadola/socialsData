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

        with self.db:
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
        # Query DB for personalities
        self.db.connect()
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id FROM personalities")
        ids = [row[0] for row in cursor.fetchall()]
        self.db.close()
        return ids

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
            "sources": [],
            "license": "Unknown"
        }

        with open(target_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        # Add to DB
        self.db.add_personality(safe_id, name, "", "")

        return safe_id

    def get_metadata(self, personality_id):
        # Try DB first? Or still file? Let's stick to file for metadata for now as source of truth for edits?
        # But we are building a DB.
        # Let's return from DB if possible, but the CLI/Tools might expect the full dictionary.
        # The DB currently stores id, name, description, system_prompt.
        # The JSON has more (sources, license).
        # So we should probably read the file, but maybe verify against DB?
        # For now, keep reading file to preserve full metadata access not yet in DB schema.
        path = self.base_dir / personality_id / "metadata.json"
        if not path.exists():
            raise FileNotFoundError(f"Personality '{personality_id}' not found.")
        with open(path, "r") as f:
            return json.load(f)
