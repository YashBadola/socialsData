import sys
from pathlib import Path

# Add project root to sys.path
# insert at 0 to prioritize local imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from socials_data.core.manager import PersonalityManager
from socials_data.core.database import DatabaseManager

def migrate():
    print("Starting migration to database...")

    # Explicitly point to local personalities dir
    local_personalities_dir = Path(__file__).parent.parent / "socials_data" / "personalities"

    pm = PersonalityManager(base_dir=local_personalities_dir)
    print(f"Base dir: {pm.base_dir.absolute()}")

    # Also need to make sure DatabaseManager puts the DB in the right place (local)
    # The default in DatabaseManager is "socials_data/philosophers.db" relative to CWD, which is fine if running from root.

    db = DatabaseManager()

    personalities = pm.list_personalities()
    print(f"Found {len(personalities)} personalities to migrate.")

    for p_id in personalities:
        try:
            metadata = pm.get_metadata(p_id)
            print(f"Migrating {metadata['name']} ({p_id})...")
            db.add_personality(metadata)
        except Exception as e:
            print(f"Error migrating {p_id}: {e}")

    print("Migration complete.")

if __name__ == "__main__":
    migrate()
