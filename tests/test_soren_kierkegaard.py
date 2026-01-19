import pytest
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset
import os
import json

def test_soren_kierkegaard_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "soren_kierkegaard" in personalities

def test_soren_kierkegaard_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("soren_kierkegaard")
    assert metadata["name"] == "Søren Kierkegaard"
    assert metadata["id"] == "soren_kierkegaard"
    assert "Fear and Trembling" in [s["title"] for s in metadata["sources"]]

def test_soren_kierkegaard_data_loaded():
    dataset = load_dataset("soren_kierkegaard")
    assert len(dataset) > 0

    # Check sample structure
    # Since the order of loading isn't guaranteed (os.listdir), we check that at least one sample is correct
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Check that sources are from the expected list
    expected_sources = ["fear_and_trembling.txt", "either_or.txt", "sickness_unto_death.txt"]
    assert sample["source"] in expected_sources

    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100

def test_processed_file_exists():
    # Construct path carefully to handle potential running from different directories
    # But current convention seems to be running from root
    processed_path = os.path.join("socials_data", "personalities", "soren_kierkegaard", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) >= 3 # We added 3 files

        sources_found = set()
        for line in lines:
            entry = json.loads(line)
            sources_found.add(entry["source"])

        assert "fear_and_trembling.txt" in sources_found
        assert "either_or.txt" in sources_found
        assert "sickness_unto_death.txt" in sources_found
