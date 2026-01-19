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
        """Returns a list of available personality IDs from the database and filesystem."""
        db_personalities = {p['id'] for p in self.db.list_personalities()}

        fs_personalities = set()
        if self.base_dir.exists():
            fs_personalities = {
                d.name for d in self.base_dir.iterdir()
                if d.is_dir() and (d / "metadata.json").exists()
            }

        return list(db_personalities | fs_personalities)

    def create_personality(self, name):
        """Creates a new personality in the database and directory structure."""
        safe_id = name.lower().replace(" ", "_").replace("-", "_")
        target_dir = self.base_dir / safe_id

        # We create the directory if it doesn't exist, just in case we want to store other things
        if not target_dir.exists():
            target_dir.mkdir()
            (target_dir / "raw").mkdir()
            (target_dir / "processed").mkdir()

        # Check if already in DB
        existing = self.db.get_personality(safe_id)
        if existing:
             # If it exists in DB, we just return the ID, or raise error?
             # The previous implementation raised FileExistsError.
             raise FileExistsError(f"Personality '{safe_id}' already exists in database.")

        self.db.add_personality(safe_id, name)

        # Also create metadata.json for backward compatibility or easy viewing
        metadata = {
            "name": name,
            "id": safe_id,
            "description": "",
            "sources": [],
            "license": "Unknown"
        }
        with open(target_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        return safe_id

    def get_metadata(self, personality_id):
        """Gets metadata from the database."""
        p = self.db.get_personality(personality_id)
        if not p:
            # Fallback to file system if not in DB (migration path)
            path = self.base_dir / personality_id / "metadata.json"
            if path.exists():
                with open(path, "r") as f:
                    return json.load(f)
            raise FileNotFoundError(f"Personality '{personality_id}' not found.")
        return p

    def add_document(self, personality_id, filename, content, source_url=""):
        """Adds a document to the database."""
        self.db.add_document(personality_id, filename, content, source_url)
