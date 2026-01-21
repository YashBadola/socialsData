
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_aristotle_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "aristotle" in personalities

def test_aristotle_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("aristotle")
    assert metadata["name"] == "Aristotle"
    assert len(metadata["sources"]) == 2

def test_aristotle_dataset_loading():
    dataset = load_dataset("aristotle")
    assert len(dataset) > 0
    # Check if we have entries from both books
    sources = set(entry["source"] for entry in dataset)
    assert "nicomachean_ethics.txt" in sources
    assert "politics.txt" in sources
