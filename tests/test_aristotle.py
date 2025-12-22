import json
import pytest
from socials_data.core.loader import load_dataset
from pathlib import Path

def test_aristotle_data_processing():
    """
    Verifies that the Aristotle dataset has been processed correctly.
    """
    dataset = load_dataset("aristotle")

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample, "Sample should contain 'text' field"
    assert "source" in sample, "Sample should contain 'source' field"

    # Check if text looks reasonable (not empty)
    assert len(sample["text"]) > 0, "Text should not be empty"

    # Check sources
    sources = set(dataset["source"])
    expected_sources = {
        "nicomachean_ethics.txt",
        "politics.txt",
        "poetics.txt",
        "de_anima.txt"
    }

    # We might not have all chunks from all files in the first few samples,
    # but we should check if at least some of the expected files are present in the whole dataset
    assert len(sources.intersection(expected_sources)) > 0, "Should contain at least some of the expected sources"

    # Check for keywords to ensure content relevance
    keywords = ["virtue", "happiness", "state", "poetry", "soul", "nature", "man", "reason"]

    found_keywords = False
    for i in range(min(100, len(dataset))):
        text = dataset[i]["text"].lower()
        if any(k in text for k in keywords):
            found_keywords = True
            break

    assert found_keywords, "Should find Aristotle-related keywords in the first 100 samples"

def test_aristotle_metadata():
    """
    Verifies the metadata for Aristotle.
    """
    base_dir = Path("socials_data/personalities/aristotle")
    metadata_path = base_dir / "metadata.json"

    assert metadata_path.exists(), "metadata.json should exist"

    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    assert metadata["id"] == "aristotle"
    assert metadata["name"] == "Aristotle"
    assert "system_prompt" in metadata
    assert len(metadata["sources"]) == 4
