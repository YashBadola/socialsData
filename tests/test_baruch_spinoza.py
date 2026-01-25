import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

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

def test_baruch_spinoza_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("baruch_spinoza")
    assert len(dataset) == 4

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Check for presence of all parts
    sources = set(d["source"] for d in dataset)
    assert "ethics_part1_definitions.txt" in sources
    assert "ethics_part1_axioms.txt" in sources
    assert "ethics_part1_propositions.txt" in sources
    assert "ethics_part2_excerpt.txt" in sources

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "baruch_spinoza", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 4
