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
    # Check that sources include the titles we added
    titles = [s["title"] for s in metadata["sources"]]
    assert "Either/Or" in titles
    assert "Fear and Trembling" in titles

def test_soren_kierkegaard_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("soren_kierkegaard")
    assert len(dataset) > 0

    # We expect 3 records corresponding to the 3 files
    assert len(dataset) == 3

    # Check that we have sources we expect
    sources = set(item['source'] for item in dataset)
    expected_sources = {"either_or.txt", "fear_and_trembling.txt", "sickness_unto_death.txt"}
    assert sources == expected_sources

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "soren_kierkegaard", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        assert len(lines) == 3
        for line in lines:
            entry = json.loads(line)
            assert "text" in entry
            assert "source" in entry
