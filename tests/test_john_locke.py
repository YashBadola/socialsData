import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_load_john_locke_dataset():
    """Test loading the John Locke dataset."""
    # Ensure local path is used
    try:
        ds = load_dataset("john_locke")
    except Exception as e:
        pytest.fail(f"Failed to load dataset: {e}")

    assert len(ds) > 0, "Dataset should not be empty"

    # Check sample content
    sample = ds[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Verify content relevance
    # Combine some text to search for keywords
    combined_text = " ".join(ds[:100]["text"]).lower()
    keywords = ["government", "understanding", "ideas", "mind", "power", "nature"]
    found = any(k in combined_text for k in keywords)
    assert found, "Dataset should contain relevant philosophical keywords"

    # Verify specific sources are present in the 'source' column
    sources = set(ds["source"])
    expected_sources = {
        "second_treatise_of_government.txt",
        "essay_concerning_human_understanding_1.txt",
        "essay_concerning_human_understanding_2.txt"
    }
    # We check if at least one of the expected sources is present (or all depending on chunking)
    assert not sources.isdisjoint(expected_sources), f"Expected sources not found. Found: {sources}"

def test_john_locke_metadata():
    """Test John Locke metadata integrity."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("john_locke")

    assert metadata["name"] == "John Locke"
    assert "Father of Liberalism" in metadata["description"]
    assert len(metadata["sources"]) == 3
    assert metadata["license"] == "Public Domain"
