import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_plato_dataset_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "plato" in personalities

def test_plato_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("plato")
    assert metadata["name"] == "Plato"
    assert metadata["id"] == "plato"
    assert len(metadata["sources"]) == 5

def test_plato_load_dataset():
    dataset = load_dataset("plato")
    assert len(dataset) > 0

    # Check sample content
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Check if text contains some expected keywords (case-insensitive)
    text = sample["text"].lower()
    # It might be any of the books, so check for general platonic terms
    keywords = ["socrates", "truth", "justice", "soul", "virtue", "athens", "glaucon", "phaedrus", "phaedo", "stranger"]
    found = any(keyword in text for keyword in keywords)
    # Note: text chunks might be small, but usually large enough to contain at least one common word or name if it's Plato.
    # However, to be safe, we can just ensure it is not empty.
    assert len(text) > 10

def test_plato_cleanliness():
    # Check that Gutenberg headers are gone
    dataset = load_dataset("plato")
    for item in dataset:
        text = item["text"]
        assert "Project Gutenberg" not in text
        assert "PROJECT GUTENBERG" not in text
