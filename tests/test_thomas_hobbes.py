import os
import json
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_load_dataset_thomas_hobbes():
    """Test that the Thomas Hobbes dataset can be loaded correctly."""
    dataset = load_dataset("thomas_hobbes")

    # Check that it's a Dataset object (it behaves like a list/dict)
    assert len(dataset) > 0

    # Check the content of the first sample
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] == "leviathan.txt"

    # Check for specific content
    text = sample["text"]
    assert "Leviathan" in text
    assert "Nature hath made men so equal" in text or "nasty, brutish, and short" in text or "Commonwealth" in text

def test_metadata_thomas_hobbes():
    """Test that the metadata for Thomas Hobbes is correct."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("thomas_hobbes")

    assert metadata["id"] == "thomas_hobbes"
    assert metadata["name"] == "Thomas Hobbes"
    assert "Leviathan" in metadata["description"]
    assert len(metadata["sources"]) > 0
    assert metadata["sources"][0]["title"] == "Leviathan"

if __name__ == "__main__":
    pytest.main([__file__])
