import os
import pytest
from socials_data.core.loader import load_dataset

def test_load_wittgenstein_dataset():
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
    expected_sources = {"tractatus.txt"}

    # We might have more files in the future, but at least tractatus should be there
    assert sources.issubset(expected_sources) or expected_sources.issubset(sources), f"Expected sources mismatch. Found: {sources}"

    # Specific keywords we expect in Wittgenstein's text (Tractatus)
    keywords = ["proposition", "world", "logic", "silence", "ladder"]
    found_keywords = False

    # Since we might have one large chunk, we check inside it
    for item in dataset:
        content = item["text"].lower()
        for keyword in keywords:
            if keyword in content:
                found_keywords = True
                # We found at least one, that's good enough to verify it's the right text
                break
        if found_keywords:
            break

    assert found_keywords, "Did not find expected keywords in the dataset"

if __name__ == "__main__":
    test_load_wittgenstein_dataset()
