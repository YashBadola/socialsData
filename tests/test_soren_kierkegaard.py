import os
import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

def test_soren_kierkegaard_dataset_exists():
    """Test that the Søren Kierkegaard dataset exists and loads correctly."""
    dataset = load_dataset("soren_kierkegaard")
    assert dataset is not None
    assert len(dataset) > 0

    # Check the first sample
    sample = dataset[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Check for some expected content (case insensitive)
    # "Kierkegaard" or "existential" or typical words from his works
    text_content = " ".join([d["text"] for d in dataset])
    assert "Kierkegaard" in text_content or "God" in text_content or "individual" in text_content

def test_soren_kierkegaard_metadata():
    """Test that the metadata is correct."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("soren_kierkegaard")

    assert metadata["name"] == "Søren Kierkegaard"
    assert metadata["id"] == "soren_kierkegaard"
    assert "existentialist" in metadata["description"]
    assert len(metadata["sources"]) > 0
    assert metadata["sources"][0]["title"] == "Selections from the Writings of Kierkegaard"

if __name__ == "__main__":
    # Allow running this test file directly
    pytest.main([__file__])
