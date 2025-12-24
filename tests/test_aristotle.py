import os
import pytest
from socials_data import load_dataset

def test_aristotle_dataset():
    # Load dataset
    ds = load_dataset("aristotle")

    # Basic checks
    assert len(ds) > 0, "Dataset should not be empty"

    # Check sample
    sample = ds[0]
    assert "text" in sample
    assert "source" in sample

    # Check content relevance (naive check)
    # Combine some text to search for keywords
    all_text = " ".join([d["text"] for d in ds])

    keywords = ["virtue", "happiness", "state", "poetry", "imitation", "category"]
    for kw in keywords:
        assert kw in all_text.lower(), f"Keyword '{kw}' not found in dataset"

    # Check for unwanted artifacts
    assert "project gutenberg" not in all_text.lower(), "Gutenberg license text should be cleaned"
