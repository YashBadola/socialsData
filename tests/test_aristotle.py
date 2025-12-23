import pytest
import os
from socials_data.core.loader import load_dataset

def test_aristotle_dataset():
    # Test that the dataset loads correctly
    dataset = load_dataset("aristotle")
    assert dataset is not None, "Dataset should not be None"

    # Check that we have some data
    assert len(dataset) > 0, "Dataset should have entries"

    # Check structure of the first item
    item = dataset[0]
    assert "text" in item, "Item should have 'text' field"
    assert "source" in item, "Item should have 'source' field"

    # Check sources
    sources = set(dataset["source"])
    expected_sources = {
        "nicomachean_ethics.txt",
        "politics.txt",
        "poetics.txt",
        "the_categories.txt"
    }

    # It's possible not all chunks from all files are in the first few items if shuffled,
    # but since load_dataset usually returns the whole thing, we can check.
    # Actually, check if expected sources are present in the dataset
    assert expected_sources.issubset(sources), f"Expected sources {expected_sources} not all found in {sources}"

    # Check content of a sample text to ensure it's not garbage or license info
    # We'll check for some keywords likely to be in Aristotle's work
    text_content = " ".join(dataset[:10]["text"]).lower()
    keywords = ["virtue", "state", "good", "nature", "man", "mean", "cause"]

    found_keywords = [kw for kw in keywords if kw in text_content]
    assert len(found_keywords) > 0, f"None of the keywords {keywords} found in the first 10 chunks."

if __name__ == "__main__":
    pytest.main([__file__])
