import os
import pytest
from socials_data.core.loader import load_dataset

def test_load_ludwig_wittgenstein_dataset():
    """Test that the Ludwig Wittgenstein dataset can be loaded and contains valid data."""
    dataset = load_dataset("ludwig_wittgenstein")

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check the structure of the first item
    first_item = dataset[0]
    assert "text" in first_item, "Item should contain 'text' field"
    assert "source" in first_item, "Item should contain 'source' field"

    # Check content of the text
    text = first_item["text"]
    assert isinstance(text, str), "Text should be a string"
    assert len(text) > 0, "Text should not be empty"

    # Check sources
    sources = set(item["source"] for item in dataset)
    expected_sources = {"tractatus.txt", "investigations.txt"}
    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"

    # Specific keywords we expect
    # We aggregate all text to search efficiently
    all_text = " ".join(item["text"] for item in dataset)

    keywords = ["world", "case", "facts", "language-game", "beetle", "fly", "bottle"]
    missing_keywords = [kw for kw in keywords if kw not in all_text]

    # Note: 'beetle' might not be in the excerpt I chose. I should check.
    # The excerpt in my thought process didn't include the beetle box analogy.
    # I should update the keywords to match what I actually put in.
    # I put in "fly", "bottle", "world", "case", "facts", "language-game".

    real_keywords = ["world", "case", "facts", "language-game", "fly", "bottle"]
    missing_real = [kw for kw in real_keywords if kw not in all_text]

    assert not missing_real, f"Missing expected keywords: {missing_real}"

if __name__ == "__main__":
    test_load_ludwig_wittgenstein_dataset()
