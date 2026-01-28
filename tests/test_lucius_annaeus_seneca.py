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
    assert "Moral Letters to Lucilius" in [s["title"] for s in metadata["sources"]]

def test_seneca_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("lucius_annaeus_seneca")
    assert len(dataset) > 0
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    # Our source file logic:
    assert "letters_from_a_stoic_excerpts.txt" in sample["source"]
    assert "Greetings from Seneca" in sample["text"]

def test_processed_files_exist():
    base_path = os.path.join("socials_data", "personalities", "lucius_annaeus_seneca", "processed")

    # Check data.jsonl
    data_path = os.path.join(base_path, "data.jsonl")
    assert os.path.exists(data_path)
    with open(data_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) >= 1
        entry = json.loads(lines[0])
        assert "text" in entry

    # Check qa.jsonl
    qa_path = os.path.join(base_path, "qa.jsonl")
    assert os.path.exists(qa_path)
    with open(qa_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) >= 6
        entry = json.loads(lines[0])
        assert "instruction" in entry
        assert "response" in entry
