import pytest
import os
import json
from socials_data.core.loader import load_dataset

@pytest.fixture
def machiavelli_dir():
    return os.path.join("socials_data", "personalities", "niccolo_machiavelli")

def test_machiavelli_exists(machiavelli_dir):
    assert os.path.exists(machiavelli_dir)
    assert os.path.exists(os.path.join(machiavelli_dir, "metadata.json"))
    assert os.path.exists(os.path.join(machiavelli_dir, "raw"))
    assert os.path.exists(os.path.join(machiavelli_dir, "processed"))

def test_machiavelli_metadata(machiavelli_dir):
    with open(os.path.join(machiavelli_dir, "metadata.json")) as f:
        metadata = json.load(f)

    assert metadata["id"] == "niccolo_machiavelli"
    assert "Niccolo Machiavelli" in metadata["name"]
    assert "System Prompt" not in metadata # Keys are usually snake_case or specific
    assert "system_prompt" in metadata
    assert "Prince" in metadata["description"]
    assert len(metadata["sources"]) >= 3

def test_machiavelli_processed_data():
    dataset = load_dataset("niccolo_machiavelli")
    assert len(dataset) > 0

    # Check a sample
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert len(sample["text"]) > 0

    # Check for content relevant to Machiavelli
    # We can check for keywords like "prince", "state", "virtue", "fortune" in the whole dataset
    # but a simple check is enough.

    # Also ensure no Gutenberg headers
    for item in dataset:
        assert "START OF THE PROJECT GUTENBERG" not in item["text"]
        assert "END OF THE PROJECT GUTENBERG" not in item["text"]
