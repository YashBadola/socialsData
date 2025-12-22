
import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

def test_epictetus_dataset_loading():
    """Test that the Epictetus dataset loads correctly."""
    dataset = load_dataset("epictetus")
    assert dataset is not None
    assert len(dataset) > 0

    # Check if the text contains expected content
    # The first few samples should contain some text
    sample = dataset[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Ensure source metadata is present if expected (based on memory)
    # The memory said processed/data.jsonl schema is {"text": "...", "source": "..."}
    assert "source" in sample

def test_epictetus_metadata():
    """Test that Epictetus metadata is correct."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("epictetus")

    assert metadata["name"] == "Epictetus"
    assert metadata["id"] == "epictetus"
    assert "Stoic" in metadata["description"]
    assert len(metadata["sources"]) > 0
    assert metadata["sources"][0]["title"] == "Discourses and Enchiridion"
