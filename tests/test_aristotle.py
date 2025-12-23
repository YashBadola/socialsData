
import pytest
import os
import json
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

@pytest.fixture
def aristotle_id():
    return "aristotle"

def test_aristotle_dataset_loading(aristotle_id):
    """Test that the Aristotle dataset loads correctly using load_dataset."""
    dataset = load_dataset(aristotle_id)
    assert dataset is not None
    # Check if it has the expected columns (text, source)
    # The dataset object might be a DatasetDict or a Dataset.
    # Usually load_dataset returns a Dataset if split is not specified or if there's only one split.
    # Based on memory, "When slicing a Hugging Face Dataset object... it returns a dictionary of lists".

    # Let's check a sample
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

def test_aristotle_metadata_content(aristotle_id):
    """Test that the metadata for Aristotle is correct."""
    # We can't import metadata.json directly, so we use PersonalityManager
    manager = PersonalityManager()
    metadata = manager.get_metadata(aristotle_id)

    assert metadata["name"] == "Aristotle"
    assert metadata["id"] == "aristotle"
    assert "system_prompt" in metadata
    assert "sources" in metadata
    assert len(metadata["sources"]) == 3

    source_titles = [s["title"] for s in metadata["sources"]]
    assert "The Nicomachean Ethics" in source_titles
    assert "Politics" in source_titles
    assert "The Poetics" in source_titles

def test_aristotle_content_validity(aristotle_id):
    """Test that the content of the dataset actually resembles Aristotle's work."""
    dataset = load_dataset(aristotle_id)

    # Check for keywords that should appear in Aristotle's works
    keywords = ["virtue", "state", "tragedy", "happiness", "mean", "cause", "political"]

    # We'll check a subset of the data to ensure at least some keywords appear
    found_keywords = set()
    for i in range(min(100, len(dataset))):
        text = dataset[i]["text"].lower()
        for kw in keywords:
            if kw in text:
                found_keywords.add(kw)

    # We expect to find at least a few of these keywords
    assert len(found_keywords) > 0, "No relevant keywords found in the first 100 samples."

def test_aristotle_sources_present(aristotle_id):
    """Test that all three processed sources are present in the dataset."""
    dataset = load_dataset(aristotle_id)
    sources = set(dataset["source"])

    expected_sources = {"nicomachean_ethics.txt", "politics.txt", "poetics.txt"}

    # Check if all expected sources are present in the 'source' column
    # Note: It's possible that data processing might drop small files or chunks,
    # but these are large books, so they should be there.
    for source in expected_sources:
        assert source in sources, f"Source {source} not found in processed dataset."
