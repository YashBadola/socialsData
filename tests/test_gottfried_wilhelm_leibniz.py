import json
import pytest
from socials_data.core.loader import load_dataset
from pathlib import Path

def test_load_dataset_leibniz():
    """Test loading the Leibniz dataset."""
    dataset = load_dataset("gottfried_wilhelm_leibniz")
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check first item
    item = dataset[0]
    assert "text" in item
    assert "source" in item
    assert isinstance(item["text"], str)
    assert len(item["text"]) > 0

def test_dataset_content_leibniz():
    """Test content of the Leibniz dataset."""
    dataset = load_dataset("gottfried_wilhelm_leibniz")

    # Check for keywords
    keywords = ["monad", "substance", "god", "perfection", "harmony"]
    found_keywords = {kw: False for kw in keywords}

    for item in dataset:
        text = item["text"].lower()
        for kw in keywords:
            if kw in text:
                found_keywords[kw] = True

    # Assert all keywords are found across the dataset
    for kw, found in found_keywords.items():
        assert found, f"Keyword '{kw}' not found in dataset"

def test_metadata_leibniz():
    """Test metadata for Leibniz."""
    metadata_path = Path("socials_data/personalities/gottfried_wilhelm_leibniz/metadata.json")
    assert metadata_path.exists()

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    assert metadata["name"] == "Gottfried Wilhelm Leibniz"
    assert metadata["id"] == "gottfried_wilhelm_leibniz"
    assert "system_prompt" in metadata
    assert "monad" in metadata["system_prompt"].lower()
