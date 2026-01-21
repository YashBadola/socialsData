import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from socials_data.core.manager import PersonalityManager
from socials_data.core.database import DatabaseManager

def migrate():
    print("Starting migration to database...")

    # Point explicitly to the local personalities directory
    personalities_dir = PROJECT_ROOT / "socials_data" / "personalities"
    db_path = PROJECT_ROOT / "socials_data" / "philosophers.db"

    print(f"Reading personalities from: {personalities_dir}")
    print(f"Writing database to: {db_path}")

    pm = PersonalityManager(base_dir=personalities_dir)
    db = DatabaseManager(db_path=str(db_path))

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
