import sqlite3
from pathlib import Path
import sys

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from socials_data.core.database import DatabaseManager

def verify():
    db = DatabaseManager()
    personalities = db.list_personalities()
    print(f"Total personalities in DB: {len(personalities)}")

    found_kierkegaard = False
    for p in personalities:
        print(f"- {p['name']} (Sources: {len(p['sources'])})")
        if p['id'] == 'soren_kierkegaard':
            found_kierkegaard = True
            print("  [VERIFIED] Kierkegaard found.")
            print(f"  System Prompt: {p['system_prompt'][:50]}...")

    if found_kierkegaard:
        print("\nSUCCESS: Søren Kierkegaard is in the database.")
    else:
        print("\nFAILURE: Søren Kierkegaard is NOT in the database.")

if __name__ == "__main__":
    verify()
