import os
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
    assert metadata["id"] == "aristotle"
    assert len(metadata["sources"]) == 3
    assert metadata["license"] == "Public Domain"

def test_aristotle_dataset_loading():
    dataset = load_dataset("aristotle")
    assert dataset is not None
    assert len(dataset) > 0

    # Check that we have content from each book
    sources = set()
    for item in dataset:
        sources.add(item["source"])
        assert "text" in item
        assert len(item["text"]) > 0

    assert "nicomachean_ethics.txt" in sources
    assert "politics.txt" in sources
    assert "poetics.txt" in sources

def test_aristotle_content_samples():
    dataset = load_dataset("aristotle")

    # Look for key concepts to ensure correct content
    text_corpus = " ".join([item["text"] for item in dataset])

    assert "eudaimonia" in text_corpus.lower() or "happiness" in text_corpus.lower()
    assert "virtue" in text_corpus.lower()
    assert "tragedy" in text_corpus.lower()

    # Negative assertion: Ensure Gutenberg headers are gone
    assert "Project Gutenberg" not in text_corpus
    assert "START OF THE PROJECT GUTENBERG EBOOK" not in text_corpus
