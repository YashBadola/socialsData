import json
import pytest
from socials_data.core.loader import load_dataset
from pathlib import Path

def test_load_dataset_ludwig_wittgenstein():
    """Test loading the Ludwig Wittgenstein dataset."""
    dataset = load_dataset("ludwig_wittgenstein")
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check first item
    item = dataset[0]
    assert "text" in item
    assert "source" in item
    assert isinstance(item["text"], str)
    assert len(item["text"]) > 0

def test_dataset_content_ludwig_wittgenstein():
    """Test content of the Ludwig Wittgenstein dataset."""
    dataset = load_dataset("ludwig_wittgenstein")

    # Check for keywords from both early and late periods
    keywords = ["world", "fact", "picture", "game", "language", "meaning", "use"]
    found_keywords = {kw: False for kw in keywords}

    for item in dataset:
        text = item["text"].lower()
        for kw in keywords:
            if kw in text:
                found_keywords[kw] = True

    # Assert all keywords are found across the dataset
    for kw, found in found_keywords.items():
        assert found, f"Keyword '{kw}' not found in dataset"

def test_metadata_ludwig_wittgenstein():
    """Test metadata for Ludwig Wittgenstein."""
    metadata_path = Path("socials_data/personalities/ludwig_wittgenstein/metadata.json")
    assert metadata_path.exists()

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    assert metadata["name"] == "Ludwig Wittgenstein"
    assert metadata["id"] == "ludwig_wittgenstein"
    assert "system_prompt" in metadata
    assert "language" in metadata["system_prompt"].lower()
    assert "logic" in metadata["system_prompt"].lower()
