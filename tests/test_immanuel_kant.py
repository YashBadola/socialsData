import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_immanuel_kant_load_dataset():
    """Test that the Immanuel Kant dataset can be loaded."""
    dataset = load_dataset("immanuel_kant")
    assert dataset is not None, "Dataset should not be None"

    # Check if we have data
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check the first item
    item = dataset[0]
    assert "text" in item, "Item should have 'text' field"
    assert "source" in item, "Item should have 'source' field"
    assert isinstance(item["text"], str), "Text should be a string"
    assert len(item["text"]) > 0, "Text should not be empty"

def test_immanuel_kant_content():
    """Test specific content in the Immanuel Kant dataset to verify correct files."""
    dataset = load_dataset("immanuel_kant")

    # We expect terms like "a priori", "reason", "imperative"
    found_term = False
    for i in range(min(len(dataset), 100)):
        text = dataset[i]["text"].lower()
        if "reason" in text or "priori" in text or "imperative" in text:
            found_term = True
            break

    assert found_term, "Should find Kantian terms in the dataset"

def test_metadata_completeness():
    manager = PersonalityManager()
    metadata = manager.get_metadata("immanuel_kant")

    assert metadata["name"] == "Immanuel Kant"
    assert metadata["id"] == "immanuel_kant"
    assert "system_prompt" in metadata
    assert len(metadata["sources"]) == 3
