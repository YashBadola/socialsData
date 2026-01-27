import json
import pytest
from socials_data.core.loader import load_dataset
from pathlib import Path

def test_load_dataset_soren_kierkegaard():
    """Test loading the Soren Kierkegaard dataset."""
    dataset = load_dataset("soren_kierkegaard")
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check first item
    item = dataset[0]
    assert "text" in item
    assert "source" in item
    assert isinstance(item["text"], str)
    assert len(item["text"]) > 0

def test_dataset_content_soren_kierkegaard():
    """Test content of the Soren Kierkegaard dataset."""
    dataset = load_dataset("soren_kierkegaard")

    # Check for keywords
    keywords = ["despair", "faith", "individual", "sickness", "paradox"]
    found_keywords = {kw: False for kw in keywords}

    for item in dataset:
        text = item["text"].lower()
        for kw in keywords:
            if kw in text:
                found_keywords[kw] = True

    # Assert all keywords are found across the dataset
    for kw, found in found_keywords.items():
        assert found, f"Keyword '{kw}' not found in dataset"

def test_metadata_soren_kierkegaard():
    """Test metadata for Soren Kierkegaard."""
    metadata_path = Path("socials_data/personalities/soren_kierkegaard/metadata.json")
    assert metadata_path.exists()

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    assert metadata["name"] == "Søren Kierkegaard"
    assert metadata["id"] == "soren_kierkegaard"
    assert "system_prompt" in metadata
    assert "existentialist" in metadata["description"].lower()
