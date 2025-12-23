import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager
import json
import os

def test_aristotle_personality_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "aristotle" in personalities

def test_aristotle_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("aristotle")
    assert metadata["name"] == "Aristotle"
    assert len(metadata["sources"]) == 4
    assert "Nicomachean Ethics" in [s["title"] for s in metadata["sources"]]

def test_aristotle_dataset_loading():
    dataset = load_dataset("aristotle")
    assert len(dataset) > 0

    # Check sample
    sample = dataset[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100

def test_aristotle_content_keywords():
    dataset = load_dataset("aristotle")
    # Convert to list to search through a few samples
    # Just check the first 50 samples for some keywords
    found_ethics = False
    found_politics = False

    keywords = ["virtue", "happiness", "state", "city", "good", "mean", "political", "tragedy", "poetry", "substance", "category"]

    for i in range(min(len(dataset), 100)):
        text = dataset[i]["text"].lower()
        if any(k in text for k in keywords):
            found_ethics = True # Loose check, but ensures we have relevant text
            break

    assert found_ethics, "Did not find expected Aristotelian keywords in the first 100 samples"
