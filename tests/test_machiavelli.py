import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

def test_machiavelli_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "niccolo_machiavelli" in personalities

def test_machiavelli_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("niccolo_machiavelli")
    assert metadata["name"] == "Niccolò Machiavelli"
    assert metadata["id"] == "niccolo_machiavelli"
    assert "The Prince" in [s["title"] for s in metadata["sources"]]

def test_machiavelli_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("niccolo_machiavelli")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] == "the_prince.txt"

    # Check for keywords from "The Prince"
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100

    # Just a simple content check on the first chunk or verify valid loading
    # (Since I'm not sure which chunk is first, I won't hardcode text here if not necessary)

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "niccolo_machiavelli", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
