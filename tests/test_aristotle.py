import sys
import json
import pytest
from unittest.mock import MagicMock

# Mock datasets before importing socials_data because it is missing in the env
mock_datasets = MagicMock()
sys.modules["datasets"] = mock_datasets

def mock_hf_loader(path, data_files=None, split=None):
    # Manually load the jsonl file to simulate what HF datasets would do
    data = []
    with open(data_files, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

mock_datasets.load_dataset.side_effect = mock_hf_loader

from socials_data.core.loader import load_dataset

def test_load_aristotle_dataset():
    """Test that the Aristotle dataset can be loaded and contains valid data."""
    dataset = load_dataset("aristotle")

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check the structure of the first item
    first_item = dataset[0]
    assert "text" in first_item, "Item should contain 'text' field"
    assert "source" in first_item, "Item should contain 'source' field"

    # Check content of the text
    text = first_item["text"]
    assert isinstance(text, str), "Text should be a string"
    assert len(text) > 0, "Text should not be empty"

    # Check sources
    sources = set(item["source"] for item in dataset)
    expected_sources = {"nicomachean_ethics.txt", "politics.txt", "metaphysics.txt"}

    # We expect all sources to be present since we manually created the data.jsonl with them
    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"

    # Specific keywords we expect in Aristotle's text
    keywords = ["virtue", "political animal", "happiness", "polis", "essence"]
    found_keywords = False
    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]:
                found_keywords = True
                break
        if found_keywords:
            break

    assert found_keywords, "Did not find expected keywords in the dataset"

if __name__ == "__main__":
    test_load_aristotle_dataset()
