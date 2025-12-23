import os
import pytest
from socials_data import load_dataset

def test_load_rousseau_dataset():
    """Test that the Jean-Jacques Rousseau dataset loads correctly."""
    dataset = load_dataset("jean_jacques_rousseau")

    # Check that it returns a Dataset object (has features, etc.)
    assert hasattr(dataset, "features")
    assert len(dataset) > 0

    # Check the schema
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert isinstance(sample["source"], str)

def test_rousseau_content_keywords():
    """Test that the dataset contains expected keywords."""
    dataset = load_dataset("jean_jacques_rousseau")

    # Collect a sample of text to check for keywords
    # We take a few samples to ensure coverage
    samples = dataset[:20]["text"]
    combined_text = " ".join(samples).lower()

    keywords = ["nature", "man", "society", "contract", "inequality"]

    for keyword in keywords:
        assert keyword in combined_text, f"Keyword '{keyword}' not found in the first 20 samples."

def test_rousseau_sources():
    """Test that all expected sources are present in the dataset."""
    dataset = load_dataset("jean_jacques_rousseau")

    sources = set(dataset["source"])
    expected_sources = {
        "the_social_contract_and_discourses.txt",
        "the_confessions.txt",
        "emile.txt"
    }

    # Check that we have at least these sources (there might be chunking effects, but filenames should match)
    for source in expected_sources:
        assert source in sources, f"Source '{source}' missing from dataset."
