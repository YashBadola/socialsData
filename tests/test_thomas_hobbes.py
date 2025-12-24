import os
import json
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_thomas_hobbes_data():
    # 1. Verify Personality Exists
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "thomas_hobbes" in personalities

    # 2. Verify Metadata
    metadata_path = manager.base_dir / "thomas_hobbes" / "metadata.json"
    assert metadata_path.exists()

    with open(metadata_path, "r") as f:
        meta = json.load(f)
        assert meta["name"] == "Thomas Hobbes"
        assert "Leviathan" in meta["sources"][0]["title"]
        assert meta["id"] == "thomas_hobbes"

    # 3. Verify Raw File Exists
    raw_file = manager.base_dir / "thomas_hobbes" / "raw" / "leviathan.txt"
    assert raw_file.exists()
    assert raw_file.stat().st_size > 0

    # 4. Verify Dataset Loads
    # Note: load_dataset uses the 'socials_data' structure.
    # Depending on implementation, it might load from processed/data.jsonl
    ds = load_dataset("thomas_hobbes")

    # Check it's not empty
    assert len(ds) > 0

    # Check content of first sample
    sample = ds[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] == "leviathan.txt"

    # Check for specific keywords expected in Hobbes
    text = sample["text"]
    # Since we have the whole book in one chunk or few chunks, let's search in the first one
    # Note: TextDataProcessor might chunk it if we implemented chunking, but for now it's likely one big chunk
    # or the test should handle iterating.

    # "Leviathan" or "Commonwealth" or "Nature" should be there.
    assert "Leviathan" in text or "Commonwealth" in text or "Nature" in text

if __name__ == "__main__":
    # Manually run if executed as script
    test_thomas_hobbes_data()
    print("Test passed!")
