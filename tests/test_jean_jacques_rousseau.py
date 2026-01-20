import json
import pytest
from socials_data.core.loader import load_dataset
from pathlib import Path

def test_load_dataset_jean_jacques_rousseau():
    """Test loading the Jean-Jacques Rousseau dataset."""
    dataset = load_dataset("jean_jacques_rousseau")
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check first item
    item = dataset[0]
    assert "text" in item
    assert "source" in item
    assert isinstance(item["text"], str)
    assert len(item["text"]) > 0

def test_dataset_content_jean_jacques_rousseau():
    """Test content of the Jean-Jacques Rousseau dataset."""
    dataset = load_dataset("jean_jacques_rousseau")

    # Check for keywords
    keywords = ["inequality", "nature", "contract", "society", "education", "freedom"]
    found_keywords = {kw: False for kw in keywords}

    for item in dataset:
        text = item["text"].lower()
        for kw in keywords:
            if kw in text:
                found_keywords[kw] = True

    # Assert all keywords are found across the dataset
    for kw, found in found_keywords.items():
        assert found, f"Keyword '{kw}' not found in dataset"

def test_metadata_jean_jacques_rousseau():
    """Test metadata for Jean-Jacques Rousseau."""
    metadata_path = Path("socials_data/personalities/jean_jacques_rousseau/metadata.json")
    assert metadata_path.exists()

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    assert metadata["name"] == "Jean-Jacques Rousseau"
    assert metadata["id"] == "jean_jacques_rousseau"
    assert "system_prompt" in metadata
    assert "chains" in metadata["system_prompt"].lower()
