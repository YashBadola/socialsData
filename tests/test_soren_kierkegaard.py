import pytest
from socials_data.core.manager import PersonalityManager
import os
import json
from socials_data import load_dataset

def test_soren_kierkegaard_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "soren_kierkegaard" in personalities

def test_soren_kierkegaard_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("soren_kierkegaard")
    assert metadata["name"] == "Søren Kierkegaard"
    assert metadata["id"] == "soren_kierkegaard"
    # Check for sources
    titles = [s["title"] for s in metadata["sources"]]
    assert "Fear and Trembling" in titles
    assert "Either/Or" in titles
    assert "The Sickness Unto Death" in titles

def test_soren_kierkegaard_data_loaded():
    dataset = load_dataset("soren_kierkegaard")
    assert len(dataset) > 0

    # Check that we can find content from each file
    sources_found = set()
    for item in dataset:
        assert "text" in item
        assert "source" in item
        sources_found.add(item["source"])

    assert "fear_and_trembling.txt" in sources_found
    assert "sickness_unto_death.txt" in sources_found
    assert "either_or.txt" in sources_found

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "soren_kierkegaard", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
