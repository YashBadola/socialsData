import os
import json
import pytest
from socials_data.core.loader import load_dataset

def test_thomas_hobbes_exists():
    path = "socials_data/personalities/thomas_hobbes"
    assert os.path.exists(path)
    assert os.path.exists(os.path.join(path, "metadata.json"))
    assert os.path.exists(os.path.join(path, "raw", "leviathan.txt"))
    assert os.path.exists(os.path.join(path, "processed", "data.jsonl"))

def test_thomas_hobbes_metadata():
    with open("socials_data/personalities/thomas_hobbes/metadata.json", "r") as f:
        metadata = json.load(f)
    assert metadata["id"] == "thomas_hobbes"
    assert metadata["name"] == "Thomas Hobbes"
    assert len(metadata["sources"]) > 0
    assert "Leviathan" in [s["title"] for s in metadata["sources"]]

def test_load_thomas_hobbes_dataset():
    # Test loading the dataset
    ds = load_dataset("thomas_hobbes")
    assert len(ds) > 0

    # Check sample content
    sample = ds[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Check for some keywords likely to be in Leviathan
    # Since we are checking chunks, we need to iterate or just check existence in the whole dataset loosely
    # But let's check if at least one sample has "commonwealth" or "sovereign"
    found_keyword = False
    for item in ds:
        text = item["text"].lower()
        if "commonwealth" in text or "sovereign" in text or "leviathan" in text:
            found_keyword = True
            break
    assert found_keyword, "Did not find expected keywords in the dataset"
