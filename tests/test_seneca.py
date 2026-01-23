import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

def test_seneca_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "seneca" in personalities

def test_seneca_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("seneca")
    assert metadata["name"] == "Seneca the Younger"
    assert metadata["id"] == "seneca"
    assert "Moral Letters to Lucilius" in [s["title"] for s in metadata["sources"]]

def test_seneca_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("seneca")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    # Check that we have both letters
    sources = set(item["source"] for item in dataset)
    assert "letter_7.txt" in sources
    assert "letter_13.txt" in sources

    # Check content snippet
    text_content = " ".join([item["text"] for item in dataset])
    assert "crowds" in text_content or "Lucilius" in text_content

def test_seneca_qa_exists():
    processed_path = os.path.join("socials_data", "personalities", "seneca", "processed", "qa.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) >= 5
        first_entry = json.loads(lines[0])
        assert "instruction" in first_entry
        assert "response" in first_entry
        assert "imagination" in first_entry["response"] or "future" in first_entry["instruction"]
