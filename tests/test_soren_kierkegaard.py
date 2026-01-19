
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager
import os

def test_soren_kierkegaard_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "soren_kierkegaard" in personalities

def test_soren_kierkegaard_dataset_structure():
    dataset = load_dataset("soren_kierkegaard")
    assert len(dataset) > 0
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] == "fear_and_trembling.txt"
    assert "Not only in the world of commerce" in sample["text"]

def test_soren_kierkegaard_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("soren_kierkegaard")
    assert metadata["name"] == "Søren Kierkegaard"
    assert metadata["id"] == "soren_kierkegaard"
    assert "existentialist" in metadata["description"]
