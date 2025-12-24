import pytest
import os
from socials_data import load_dataset

def test_load_rene_descartes_dataset():
    """Test loading the René Descartes dataset."""
    dataset = load_dataset("rene_descartes")
    assert dataset is not None
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Check for specific keywords to ensure correct content
    # Combine some text to search
    all_text = " ".join([d["text"] for d in dataset])

    # Keywords for Descartes
    keywords = [
        "cogito", "reason", "doubt", "God", "soul", "mind", "body", "method",
        "Discourse", "Meditations"
    ]

    # We expect most keywords to be present, but check at least some distinct ones
    found_keywords = [k for k in keywords if k.lower() in all_text.lower()]
    assert len(found_keywords) >= 3, f"Found only {found_keywords}"

    # Verify sources
    sources = set(d["source"] for d in dataset)
    expected_sources = {
        "discourse_on_method.txt",
        "meditations.txt",
        "principles_of_philosophy.txt"
    }
    assert expected_sources.issubset(sources), f"Missing sources: {expected_sources - sources}"
