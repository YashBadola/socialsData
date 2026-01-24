import pytest
from socials_data.core.manager import PersonalityManager
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
    # Check source
    assert "Selections from the Writings of Kierkegaard" in [s["title"] for s in metadata["sources"]]

def test_soren_kierkegaard_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("soren_kierkegaard")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    # Check that source is one of the split files
    valid_sources = [
        "diapsalmata.txt", "fear_and_trembling.txt", "in_vino_veritas.txt",
        "introduction.txt", "preparation_for_christian_life.txt", "the_present_moment.txt"
    ]
    assert sample["source"] in valid_sources

    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "soren_kierkegaard", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        # Check a few lines
        for line in lines[:5]:
             entry = json.loads(line)
             assert "text" in entry
             assert "source" in entry
