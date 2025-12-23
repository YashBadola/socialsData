import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

PERSONALITY_ID = "jean_jacques_rousseau"

def test_personality_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert PERSONALITY_ID in personalities

def test_metadata_fields():
    manager = PersonalityManager()
    metadata = manager.get_metadata(PERSONALITY_ID)
    assert metadata["name"] == "Jean-Jacques Rousseau"
    assert metadata["id"] == PERSONALITY_ID
    assert "system_prompt" in metadata
    assert len(metadata["sources"]) == 3

def test_dataset_loading():
    dataset = load_dataset(PERSONALITY_ID)
    assert len(dataset) > 0

    # Check first few samples
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

def test_content_relevance():
    dataset = load_dataset(PERSONALITY_ID)
    # Check for keywords across a subset of data
    keywords = ["social contract", "nature", "inequality", "freedom", "education", "confessions"]
    found_keywords = set()

    for i in range(min(100, len(dataset))):
        text = dataset[i]["text"].lower()
        for kw in keywords:
            if kw in text:
                found_keywords.add(kw)

    # We expect at least some of these to appear
    assert len(found_keywords) > 0
