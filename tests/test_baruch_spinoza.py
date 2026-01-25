import pytest
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset
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
    assert "Theological-Political Treatise" in [s["title"] for s in metadata["sources"]]
    assert "Deus sive Natura" in metadata["system_prompt"]

def test_baruch_spinoza_data_loaded():
    dataset = load_dataset("baruch_spinoza")
    assert len(dataset) > 0

    # Check that we have content from different sources
    sources = set([item["source"] for item in dataset])
    assert "ethics_part1_definitions.txt" in sources
    assert "ethics_part1_axioms.txt" in sources
    assert "ethics_part1_propositions.txt" in sources
    assert "ethics_part2_excerpt.txt" in sources
    assert "theological_political_excerpt.txt" in sources

    # Check for specific Spinoza quotes
    all_text = " ".join([item["text"] for item in dataset])
    assert "God, or substance" in all_text
    assert "By that which is self-caused" in all_text

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "baruch_spinoza", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 5 # We added 5 files
