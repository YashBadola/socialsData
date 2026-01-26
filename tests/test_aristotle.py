import pytest
from socials_data.core.loader import load_dataset

def test_load_aristotle_dataset():
    """Test that the Aristotle dataset can be loaded and contains valid data."""
    dataset = load_dataset("aristotle")

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
    expected_sources = {"nicomachean_ethics.txt", "politics.txt", "metaphysics.txt"}

    # We expect all sources to be present since we added them and processed them
    assert sources == expected_sources, f"Expected sources {expected_sources}, but found {sources}"

    # Specific keywords we expect in Aristotle's text
    keywords = ["virtue", "happiness", "political animal", "being as being", "art", "nature"]
    found_keywords = set()
    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]:
                found_keywords.add(keyword)

    # Check that we found at least some relevant keywords
    assert len(found_keywords) > 0, f"Did not find any expected keywords: {keywords}"

    # Check specific famous phrases
    all_text = " ".join([item["text"] for item in dataset])
    assert "political animal" in all_text
    assert "desire to know" in all_text

if __name__ == "__main__":
    test_load_aristotle_dataset()
