import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

def test_soren_kierkegaard_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "soren_kierkegaard" in personalities

def test_soren_kierkegaard_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("soren_kierkegaard")
    assert metadata["name"] == "Søren Kierkegaard"
    assert metadata["id"] == "soren_kierkegaard"
    # Check that "Fear and Trembling" is in sources
    titles = [s["title"] for s in metadata["sources"]]
    assert "Fear and Trembling" in titles

def test_soren_kierkegaard_data_loaded():
    from socials_data.core.loader import load_dataset
    dataset = load_dataset("soren_kierkegaard")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] == "kierkegaard_writings.txt"

    # Check content
    text = sample["text"]
    assert "anxiety" in text.lower() or "despair" in text.lower()
