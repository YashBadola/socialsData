import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

def test_seneca_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "lucius_annaeus_seneca" in personalities

def test_seneca_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("lucius_annaeus_seneca")
    assert metadata["name"] == "Lucius Annaeus Seneca"
    assert metadata["id"] == "lucius_annaeus_seneca"
    assert "Epistulae Morales ad Lucilium (Letters from a Stoic)" in [s["title"] for s in metadata["sources"]]

def test_seneca_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("lucius_annaeus_seneca")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    # source order might vary depending on OS file listing, but it should be one of the files
    assert sample["source"] in ["letter_1.txt", "letter_2.txt", "on_anger.txt", "on_shortness_of_life.txt"]

    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "lucius_annaeus_seneca", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 4 # We created 4 files
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
