import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager
import json
import os

def test_load_plato_dataset():
    """Verify that the Plato dataset loads correctly using load_dataset."""
    # This might fail if the dataset is not built/packaged or if load_dataset expects a huggingface repo.
    # Based on memory, load_dataset relies on `datasets` library.
    # The local `load_dataset` likely loads from the processed directory.

    # Check if processed file exists
    processed_path = "socials_data/personalities/plato/processed/data.jsonl"
    assert os.path.exists(processed_path), "Processed data not found"

    # Load the dataset
    dataset = load_dataset("plato")

    # Verify dataset type
    assert dataset is not None
    # Depending on implementation, it might be a Dataset object or similar.

    # Verify content
    assert len(dataset) > 0
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

def test_plato_metadata():
    """Verify Plato metadata."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("plato")

    assert metadata["name"] == "Plato"
    assert metadata["id"] == "plato"
    assert "The Republic" in [s["title"] for s in metadata["sources"]]
    assert metadata["system_prompt"].startswith("You are Plato.")

def test_plato_content_relevance():
    """Verify that the dataset contains relevant keywords."""
    dataset = load_dataset("plato")

    # Flatten the dataset to search for keywords in a sample of texts
    # Taking first 100 entries or all if less
    sample_texts = [entry["text"] for entry in dataset][:100]
    full_text_sample = " ".join(sample_texts).lower()

    keywords = ["socrates", "virtue", "justice", "truth", "good", "soul"]
    for keyword in keywords:
        assert keyword in full_text_sample, f"Keyword '{keyword}' not found in sample text"
