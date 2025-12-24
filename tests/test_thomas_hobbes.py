import os
import json
import pytest
from pathlib import Path
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_thomas_hobbes_data():
    """Test that Thomas Hobbes data loads and contains expected content."""
    personality_id = "thomas_hobbes"
    manager = PersonalityManager()

    # 1. Check metadata
    metadata = manager.get_metadata(personality_id)
    assert metadata["name"] == "Thomas Hobbes"
    assert metadata["id"] == "thomas_hobbes"

    # 2. Check files exist
    base_dir = Path("socials_data/personalities/thomas_hobbes")
    assert (base_dir / "raw" / "leviathan.txt").exists()
    assert (base_dir / "processed" / "data.jsonl").exists()

    # 3. Load dataset using the loader
    # Note: load_dataset in this repo returns a Hugging Face Dataset object
    # We must ensure we are using the local package, so PYTHONPATH=. is needed when running.
    ds = load_dataset(personality_id)
    assert len(ds) > 0

    # 4. Content verification
    # Hobbes uses archaic spelling: "Soveraign", "Common-wealth", "Leviathan"

    found_commonwealth = False
    found_sovereign = False
    found_leviathan = False

    # We iterate samples.
    for row in ds:
        text = row["text"]
        # Case insensitive check might be safer, but let's check specific forms we saw.
        if "Common-wealth" in text or "Commonwealth" in text:
            found_commonwealth = True
        if "Soveraign" in text or "Sovereign" in text:
            found_sovereign = True
        if "LEVIATHAN" in text or "Leviathan" in text:
            found_leviathan = True

    assert found_commonwealth, "Did not find 'Common-wealth' in the dataset"
    assert found_sovereign, "Did not find 'Soveraign' in the dataset"
    assert found_leviathan, "Did not find 'Leviathan' in the dataset"

if __name__ == "__main__":
    # verification script style
    try:
        test_thomas_hobbes_data()
        print("Thomas Hobbes verification passed!")
    except Exception as e:
        print(f"Verification failed: {e}")
        exit(1)
