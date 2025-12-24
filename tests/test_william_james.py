import os
import json
import pytest
from socials_data.core.loader import load_dataset

def test_william_james_exists():
    path = "socials_data/personalities/william_james"
    assert os.path.exists(path)
    assert os.path.exists(os.path.join(path, "metadata.json"))
    assert os.path.exists(os.path.join(path, "raw"))
    assert os.path.exists(os.path.join(path, "processed"))

def test_metadata():
    with open("socials_data/personalities/william_james/metadata.json", "r") as f:
        data = json.load(f)
    assert data["name"] == "William James"
    assert data["id"] == "william_james"
    assert "Pragmatism" in data["system_prompt"]
    assert len(data["sources"]) >= 5

def test_raw_files():
    raw_dir = "socials_data/personalities/william_james/raw"
    files = os.listdir(raw_dir)
    assert "varieties_of_religious_experience.txt" in files
    assert "pragmatism.txt" in files
    assert "essays_in_radical_empiricism.txt" in files
    assert "a_pluralistic_universe.txt" in files
    assert "the_will_to_believe.txt" in files

def test_load_dataset():
    # Test loading the processed dataset
    dataset = load_dataset("william_james")
    assert len(dataset) > 0

    # Check a sample
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)

    # Check for content relevance
    all_text = " ".join([d["text"] for d in dataset])
    assert "pragmatism" in all_text.lower() or "religious" in all_text.lower()

    # Check for absence of Gutenberg boilerplate (basic check)
    # Note: verify that the start/end markers worked reasonable well
    # by checking we don't have massive chunks of license text at the very start
    # of the first entry of a source.

    # We can check specific known boilerplate
    assert "START OF THE PROJECT GUTENBERG" not in all_text

    # Check sources
    sources = set([d["source"] for d in dataset])
    assert "pragmatism.txt" in sources
    assert "varieties_of_religious_experience.txt" in sources
