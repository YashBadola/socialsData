import json
import pytest
from socials_data.core.loader import load_dataset
from pathlib import Path

def test_load_dataset_rene_descartes():
    """Test loading the Rene Descartes dataset."""
    dataset = load_dataset("rene_descartes")
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check first item
    item = dataset[0]
    assert "text" in item
    assert "source" in item
    assert isinstance(item["text"], str)
    assert len(item["text"]) > 0

def test_dataset_content_rene_descartes():
    """Test content of the Rene Descartes dataset."""
    dataset = load_dataset("rene_descartes")

    # Check for keywords
    keywords = ["reason", "method", "god", "soul", "thought", "doubt"]
    found_keywords = {kw: False for kw in keywords}

    for item in dataset:
        text = item["text"].lower()
        for kw in keywords:
            if kw in text:
                found_keywords[kw] = True

    # Assert all keywords are found across the dataset
    for kw, found in found_keywords.items():
        assert found, f"Keyword '{kw}' not found in dataset"

def test_metadata_rene_descartes():
    """Test metadata for Rene Descartes."""
    metadata_path = Path("socials_data/personalities/rene_descartes/metadata.json")
    assert metadata_path.exists()

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    assert metadata["name"] == "René Descartes"
    assert metadata["id"] == "rene_descartes"
    assert "system_prompt" in metadata
    assert "dualist" in metadata["system_prompt"].lower()
