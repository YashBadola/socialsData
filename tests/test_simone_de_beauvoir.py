import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

def test_simone_de_beauvoir_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "simone_de_beauvoir" in personalities

def test_simone_de_beauvoir_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("simone_de_beauvoir")
    assert metadata["name"] == "Simone de Beauvoir"
    assert metadata["id"] == "simone_de_beauvoir"
    assert "The Second Sex" in [s["title"] for s in metadata["sources"]]

def test_simone_de_beauvoir_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("simone_de_beauvoir")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    # Check that source is one of the files we created
    assert sample["source"] in ["the_ethics_of_ambiguity_ch3.txt", "the_second_sex_intro.txt", "memoirs_quotes.txt"]

    # Check for text length
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 20

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "simone_de_beauvoir", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
