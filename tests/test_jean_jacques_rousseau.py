import json
import pytest
from socials_data.core.loader import load_dataset
from datasets import Dataset

def test_load_dataset():
    dataset = load_dataset("jean_jacques_rousseau")
    assert isinstance(dataset, Dataset)
    assert len(dataset) > 0

    # Check sample
    sample = dataset[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0
    assert "source" in sample

    # Check that text content is relevant (searching for a keyword)
    # Since it's shuffled or split, we might need to search a few samples or check for general content

    # Just checking if any sample contains "man" or "society" or "inequality" or "contract"
    relevant = False
    for i in range(min(10, len(dataset))):
        text = dataset[i]["text"].lower()
        if "man" in text or "society" in text or "contract" in text or "inequality" in text or "nature" in text:
            relevant = True
            break
    assert relevant

def test_metadata_exists():
    import os
    metadata_path = "socials_data/personalities/jean_jacques_rousseau/metadata.json"
    assert os.path.exists(metadata_path)

    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    assert metadata["id"] == "jean_jacques_rousseau"
    assert "system_prompt" in metadata
    assert len(metadata["sources"]) == 2
