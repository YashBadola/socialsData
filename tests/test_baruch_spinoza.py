
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_load_dataset_spinoza():
    """Test that the Baruch Spinoza dataset loads correctly."""
    dataset = load_dataset("baruch_spinoza")
    assert dataset is not None, "Dataset failed to load."

    # Check that it has data
    assert len(dataset) > 0, "Dataset is empty."

    # Check sample content
    sample = dataset[0]
    assert "text" in sample, "Sample missing 'text' field."
    assert "source" in sample, "Sample missing 'source' field."
    assert isinstance(sample["text"], str), "'text' field is not a string."

    # Check for keywords related to Spinoza
    # Note: Using lower case for case-insensitive check
    text_content = " ".join([d["text"] for d in dataset])
    keywords = ["god", "nature", "substance", "attribute", "mode", "ethics", "understanding"]
    found_keywords = [k for k in keywords if k in text_content.lower()]
    assert len(found_keywords) > 0, f"No expected keywords found in dataset. Found: {found_keywords}"

def test_metadata_spinoza():
    """Test that metadata for Spinoza is correct."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("baruch_spinoza")

    assert metadata["name"] == "Baruch Spinoza"
    assert metadata["id"] == "baruch_spinoza"
    assert "Ethics" in [s["title"] for s in metadata["sources"]]
    assert metadata["license"] == "Public Domain"
