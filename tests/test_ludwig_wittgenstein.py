import pytest
from socials_data.core.manager import PersonalityManager
import os
import json
from socials_data import load_dataset

def test_ludwig_wittgenstein_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "ludwig_wittgenstein" in personalities

def test_ludwig_wittgenstein_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("ludwig_wittgenstein")
    assert metadata["name"] == "Ludwig Wittgenstein"
    assert metadata["id"] == "ludwig_wittgenstein"
    assert "Tractatus Logico-Philosophicus" in [s["title"] for s in metadata["sources"]]

def test_ludwig_wittgenstein_data_loaded():
    dataset = load_dataset("ludwig_wittgenstein")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] == "tractatus.txt"

    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "ludwig_wittgenstein", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
