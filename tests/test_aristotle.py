import json
import pytest
from socials_data.core.loader import load_dataset
from pathlib import Path

def test_load_dataset_aristotle():
    """Test loading the Aristotle dataset."""
    dataset = load_dataset("aristotle")
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check first item
    item = dataset[0]
    assert "text" in item
    assert "source" in item
    assert isinstance(item["text"], str)
    assert len(item["text"]) > 0

def test_dataset_content_aristotle():
    """Test content of the Aristotle dataset."""
    dataset = load_dataset("aristotle")

    # Check for keywords
    keywords = ["virtue", "reason", "happiness", "soul", "mean"]
    found_keywords = {kw: False for kw in keywords}

    for item in dataset:
        text = item["text"].lower()
        for kw in keywords:
            if kw in text:
                found_keywords[kw] = True

    # Assert all keywords are found across the dataset
    for kw, found in found_keywords.items():
        assert found, f"Keyword '{kw}' not found in dataset"

def test_metadata_aristotle():
    """Test metadata for Aristotle."""
    metadata_path = Path("socials_data/personalities/aristotle/metadata.json")
    assert metadata_path.exists()

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    assert metadata["name"] == "Aristotle"
    assert metadata["id"] == "aristotle"
    assert "system_prompt" in metadata
    assert "teleological" in metadata["system_prompt"].lower()
