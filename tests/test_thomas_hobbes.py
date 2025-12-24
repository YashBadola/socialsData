import os
import json
import pytest
from pathlib import Path
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_thomas_hobbes_data():
    """Test that the Thomas Hobbes dataset loads correctly and contains valid data."""
    # Ensure we are in the right environment
    # Note: load_dataset relies on the package being installed or in pythonpath

    # 1. Verify existence of files
    manager = PersonalityManager()
    personality_dir = manager.base_dir / "thomas_hobbes"

    assert personality_dir.exists()
    assert (personality_dir / "metadata.json").exists()
    assert (personality_dir / "raw" / "leviathan.txt").exists()
    assert (personality_dir / "processed" / "data.jsonl").exists()

    # 2. Verify Metadata
    with open(personality_dir / "metadata.json", "r") as f:
        meta = json.load(f)
        assert meta["id"] == "thomas_hobbes"
        assert meta["name"] == "Thomas Hobbes"
        assert "Leviathan" in meta["sources"][0]["title"]

    # 3. Verify Dataset Loading
    # We use load_dataset from the package
    dataset = load_dataset("thomas_hobbes")

    # Check it's not empty
    assert len(dataset) > 0

    # Check sample content
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] == "leviathan.txt"

    # Check for specific keywords in the text to ensure it's actually Hobbes
    # We might need to iterate if the first chunk is just TOC or something

    found_keyword = False
    # Check first few samples
    for i in range(min(5, len(dataset))):
        text = dataset[i]["text"].lower()
        if "commonwealth" in text or "sovereign" in text or "nature" in text or "leviathan" in text or "hobbes" in text:
            found_keyword = True
            break

    assert found_keyword, "Could not find expected keywords (commonwealth, sovereign, nature) in the first few chunks."

if __name__ == "__main__":
    test_thomas_hobbes_data()
