import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

PERSONALITY_ID = "jean_jacques_rousseau"

def test_personality_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert PERSONALITY_ID in personalities

def test_metadata_structure():
    manager = PersonalityManager()
    metadata = manager.get_metadata(PERSONALITY_ID)
    assert metadata["name"] == "Jean-Jacques Rousseau"
    assert metadata["id"] == PERSONALITY_ID
    assert "system_prompt" in metadata
    assert len(metadata["sources"]) == 3

def test_load_dataset():
    dataset = load_dataset(PERSONALITY_ID)
    # The dataset returned is a HuggingFace dataset object
    assert len(dataset) > 0

    # Check sample content
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Check keywords in text to verify content
    # Since we have 3 books, and we don't know the order in the dataset (it iterates raw files),
    # we just check that we have a significant amount of text.
    all_text = "".join(dataset["text"])
    assert "social contract" in all_text.lower() or "man is born free" in all_text.lower()
    assert "emile" in all_text.lower() or "education" in all_text.lower()
    assert "confessions" in all_text.lower() or "childhood" in all_text.lower()

def test_processed_files_exist():
    base_path = os.path.dirname(os.path.abspath(__file__))
    processed_path = os.path.join(base_path, "..", "socials_data", "personalities", PERSONALITY_ID, "processed", "data.jsonl")
    assert os.path.exists(processed_path)
