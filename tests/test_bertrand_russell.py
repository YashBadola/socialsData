import json
import pytest
from pathlib import Path
from socials_data.core.loader import load_dataset

def test_metadata_bertrand_russell():
    """Test metadata for Bertrand Russell."""
    metadata_path = Path("socials_data/personalities/bertrand_russell/metadata.json")
    assert metadata_path.exists()

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    assert metadata["name"] == "Bertrand Russell"
    assert metadata["id"] == "bertrand_russell"
    assert "system_prompt" in metadata
    assert "logic" in metadata["system_prompt"].lower()

def test_dataset_bertrand_russell():
    """Test loading and content of the Bertrand Russell dataset."""
    dataset = load_dataset("bertrand_russell")
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check structure
    item = dataset[0]
    assert "text" in item
    assert "source" in item
    assert isinstance(item["text"], str)
    assert len(item["text"]) > 0

    # Check for keywords
    keywords = ["philosophy", "knowledge", "truth", "belief", "matter"]
    found_keywords = {kw: False for kw in keywords}

    for item in dataset:
        text = item["text"].lower()
        for kw in keywords:
            if kw in text:
                found_keywords[kw] = True

    for kw, found in found_keywords.items():
        assert found, f"Keyword '{kw}' not found in dataset"
