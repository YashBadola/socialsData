
import pytest
import os
from socials_data import load_dataset

def test_load_plato_dataset():
    """Verify that the Plato dataset can be loaded and contains valid data."""
    dataset = load_dataset("plato")
    # The loader returns a Hugging Face Dataset object, which behaves like a list but isn't a list instance
    assert len(dataset) > 0, "Dataset should not be empty"

    first_item = dataset[0]
    assert "text" in first_item, "Dataset items should have a 'text' field"
    assert isinstance(first_item["text"], str), "'text' field should be a string"
    assert len(first_item["text"]) > 0, "'text' field should not be empty"

def test_plato_metadata_structure():
    """Verify that the Plato metadata structure is valid."""
    import json
    metadata_path = "socials_data/personalities/plato/metadata.json"
    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    assert metadata["name"] == "Plato"
    assert metadata["id"] == "plato"
    assert "system_prompt" in metadata
    assert len(metadata["sources"]) == 3
