import os
import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

def test_load_dataset_immanuel_kant():
    """Test loading the Immanuel Kant dataset."""
    try:
        dataset = load_dataset("immanuel_kant")
    except ValueError as e:
        pytest.fail(f"Failed to load dataset: {e}")

    assert dataset is not None
    assert len(dataset) > 0

    # Check first item structure
    item = dataset[0]
    assert "text" in item
    assert "source" in item
    assert isinstance(item["text"], str)
    assert len(item["text"]) > 0

    # Verify content relevance (basic check)
    # Combining text to check for keywords, as the first chunk might be just intro
    # When slicing a dataset (dataset[:5]), it returns a dict of lists, e.g., {'text': [...], 'source': [...]}
    combined_text = "".join(dataset[:5]["text"]).lower()

    keywords = ["reason", "pure", "practical", "kant", "critique", "transcendental", "law", "moral"]
    assert any(keyword in combined_text for keyword in keywords), \
        f"None of the expected keywords {keywords} found in the first 5 chunks of text."

def test_metadata_structure():
    """Test the metadata for Immanuel Kant."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("immanuel_kant")

    assert metadata["name"] == "Immanuel Kant"
    assert metadata["id"] == "immanuel_kant"
    assert "critique" in metadata["sources"][0]["title"].lower()
    assert metadata["license"] == "Public Domain"

if __name__ == "__main__":
    pytest.main([__file__])
