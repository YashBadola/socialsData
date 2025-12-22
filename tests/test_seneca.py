import pytest
from socials_data import load_dataset
from datasets import Dataset

def test_seneca_dataset_loading():
    """Test that the Seneca dataset loads correctly."""
    dataset = load_dataset("seneca")
    assert isinstance(dataset, Dataset)
    assert len(dataset) > 0

    # Check first sample
    sample = dataset[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100

    # Check for characteristic keywords (case-insensitive)
    text_content = " ".join([d["text"] for d in dataset]).lower()
    assert "seneca" in text_content
    assert "virtue" in text_content or "happy" in text_content or "anger" in text_content

def test_seneca_metadata():
    """Test that Seneca metadata is valid."""
    from socials_data.core.manager import PersonalityManager
    manager = PersonalityManager()
    metadata = manager.get_metadata("seneca")

    assert metadata["name"] == "Lucius Annaeus Seneca"
    assert metadata["id"] == "seneca"
    assert "system_prompt" in metadata
    assert len(metadata["sources"]) > 0
    assert metadata["sources"][0]["license"] == "Public Domain"
