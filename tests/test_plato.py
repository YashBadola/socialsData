import os
import pytest
from socials_data import load_dataset

def test_load_plato_dataset():
    """Test that the Plato dataset can be loaded and contains expected data."""
    dataset = load_dataset("plato")

    # Check that it's a dataset
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check a sample
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Check that sources are from the expected files
    sources = set(dataset["source"])
    expected_files = {"the_republic.txt", "the_symposium.txt", "the_apology.txt"}
    # Note: source path might just be the filename
    assert any(s in expected_files for s in sources), f"Sources {sources} should contain at least one of {expected_files}"

    # Check for some Plato specific keywords in the text to verify content
    # Scanning a few samples
    found_keyword = False
    keywords = ["Socrates", "justice", "love", "virtue", "state", "soul", "gods"]

    for i in range(min(100, len(dataset))):
        text = dataset[i]["text"]
        if any(k in text for k in keywords):
            found_keyword = True
            break

    assert found_keyword, "Should find Plato-related keywords in the first 100 samples"
