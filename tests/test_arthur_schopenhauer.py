import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

def test_arthur_schopenhauer_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "arthur_schopenhauer" in personalities

def test_arthur_schopenhauer_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("arthur_schopenhauer")
    assert metadata["name"] == "Arthur Schopenhauer"
    assert metadata["id"] == "arthur_schopenhauer"
    assert "Studies in Pessimism" in [s["title"] for s in metadata["sources"]]

def test_arthur_schopenhauer_data_loaded():
    # Attempt to manually load the jsonl file to simulate loading dataset
    # effectively mirroring what load_dataset does for local files.
    processed_path = os.path.join("socials_data", "personalities", "arthur_schopenhauer", "processed", "data.jsonl")

    data = []
    with open(processed_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))

    assert len(data) > 0

    # Check if we have entries from both sources
    sources = [d["source"] for d in data]
    assert "quotes.txt" in sources
    assert "studies_in_pessimism.txt" in sources

    # Check content of one entry
    entry = next(d for d in data if d["source"] == "quotes.txt")
    assert "Talent hits a target" in entry["text"]

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "arthur_schopenhauer", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
