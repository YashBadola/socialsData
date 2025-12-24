import pytest
import os
from socials_data import load_dataset

@pytest.fixture
def aristotle_dataset():
    # Ensure we can load the dataset
    return load_dataset("aristotle")

def test_aristotle_load(aristotle_dataset):
    assert aristotle_dataset is not None
    assert len(aristotle_dataset) > 0

def test_aristotle_content(aristotle_dataset):
    # Check for keywords from the works
    text = " ".join([d["text"] for d in aristotle_dataset])
    assert "virtue" in text.lower()  # Nicomachean Ethics
    assert "state" in text.lower()   # Politics
    assert "tragedy" in text.lower() # Poetics
    assert "substance" in text.lower() # Categories

def test_no_gutenberg_headers(aristotle_dataset):
    for entry in aristotle_dataset:
        assert "START OF THE PROJECT GUTENBERG EBOOK" not in entry["text"]
        assert "END OF THE PROJECT GUTENBERG EBOOK" not in entry["text"]
        # Also check for license text that might have slipped through
        assert "Project Gutenberg License" not in entry["text"]

def test_source_metadata(aristotle_dataset):
    sources = set(d["source"] for d in aristotle_dataset)
    expected_sources = {
        "nicomachean_ethics.txt",
        "politics.txt",
        "poetics.txt",
        "the_categories.txt"
    }
    assert expected_sources.issubset(sources)
