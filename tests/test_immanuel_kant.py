import pytest
from socials_data.core.loader import load_dataset
from pathlib import Path

def test_immanuel_kant_dataset_structure():
    """Verify that the Immanuel Kant dataset loads correctly and has the expected structure."""
    dataset = load_dataset("immanuel_kant")

    assert len(dataset) > 0, "Dataset should not be empty"

    # Check the first sample
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert isinstance(sample["source"], str)

def test_immanuel_kant_content():
    """Verify that the content is relevant to Immanuel Kant."""
    dataset = load_dataset("immanuel_kant")

    # Collect all text to search for keywords
    all_text = " ".join([d["text"] for d in dataset])

    keywords = ["reason", "critique", "pure", "practical", "transcendental", "imperative"]
    found_keywords = [kw for kw in keywords if kw.lower() in all_text.lower()]

    assert len(found_keywords) > 0, f"Expected to find some keywords: {keywords}, but found: {found_keywords}"

def test_immanuel_kant_sources():
    """Verify that the sources are correct."""
    dataset = load_dataset("immanuel_kant")
    sources = set(d["source"] for d in dataset)

    expected_sources = {"critique_of_pure_reason.txt", "critique_of_practical_reason.txt"}
    assert sources.intersection(expected_sources), f"Expected sources to contain at least one of {expected_sources}, but got {sources}"
