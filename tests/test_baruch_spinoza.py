import pytest
from socials_data.core.manager import PersonalityManager
import os
import json
from socials_data import load_dataset

def test_baruch_spinoza_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "baruch_spinoza" in personalities

def test_baruch_spinoza_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("baruch_spinoza")
    assert metadata["name"] == "Baruch Spinoza"
    assert metadata["id"] == "baruch_spinoza"
    assert "Ethics" in [s["title"] for s in metadata["sources"]]
    assert "Theological-Political Treatise" in [s["title"] for s in metadata["sources"]]

def test_baruch_spinoza_data_loaded():
    dataset = load_dataset("baruch_spinoza")
    assert len(dataset) == 4

    # Check if we can find content from our files
    sources = [item["source"] for item in dataset]
    assert "ethics_part1_definitions.txt" in sources
    assert "ethics_part1_axioms.txt" in sources
    assert "ethics_part2_mind.txt" in sources
    assert "ttp_freedom.txt" in sources

    # Check content of one item
    definitions_item = next(item for item in dataset if item["source"] == "ethics_part1_definitions.txt")
    assert "By that which is self-caused" in definitions_item["text"]

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "baruch_spinoza", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 4
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
