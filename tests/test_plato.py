import os
import json
import pytest
from socials_data.core.loader import load_dataset

PERSONALITY_ID = "plato"
METADATA_PATH = f"socials_data/personalities/{PERSONALITY_ID}/metadata.json"
RAW_DIR = f"socials_data/personalities/{PERSONALITY_ID}/raw"
PROCESSED_DATA_PATH = f"socials_data/personalities/{PERSONALITY_ID}/processed/data.jsonl"

def test_metadata_exists_and_valid():
    assert os.path.exists(METADATA_PATH)
    with open(METADATA_PATH, "r") as f:
        data = json.load(f)
    assert data["id"] == PERSONALITY_ID
    assert "system_prompt" in data
    assert len(data["sources"]) >= 4

def test_raw_files_exist():
    expected_files = ["the_republic.txt", "symposium.txt", "apology.txt", "phaedo.txt"]
    for filename in expected_files:
        filepath = os.path.join(RAW_DIR, filename)
        assert os.path.exists(filepath), f"{filename} not found in raw directory"
        # Check they are not empty and not just containing error messages
        with open(filepath, "r") as f:
            content = f.read()
            assert len(content) > 1000, f"{filename} content is too short"
            assert "*** START OF THE PROJECT GUTENBERG" not in content, f"{filename} still has PG start marker"
            # Note: The Republic cleaning was refined, others used standard or generic.
            # "The Republic" should have "PERSONS OF THE DIALOGUE" early on.
            if filename == "the_republic.txt":
                assert "PERSONS OF THE DIALOGUE" in content[:1000]

def test_dataset_loads():
    ds = load_dataset(PERSONALITY_ID)
    assert len(ds) > 0
    sample = ds[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)

    # Check for specific content
    # Look for "Socrates" in at least one sample
    found_socrates = False
    for i in range(min(len(ds), 100)):
        if "Socrates" in ds[i]["text"]:
            found_socrates = True
            break
    assert found_socrates, "Socrates not found in first 100 chunks"

if __name__ == "__main__":
    # Manually run tests if executed directly
    test_metadata_exists_and_valid()
    test_raw_files_exist()
    test_dataset_loads()
    print("All Plato tests passed!")
