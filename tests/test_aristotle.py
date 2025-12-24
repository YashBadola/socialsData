import os
import json
import pytest
from socials_data.core.loader import load_dataset

# Utility to get absolute path
def get_abs_path(rel_path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), rel_path)

def test_aristotle_dataset_exists():
    """Test that the aristotle dataset loads correctly."""
    dataset = load_dataset("aristotle")
    assert dataset is not None
    assert len(dataset) > 0

def test_aristotle_content():
    """Test that the content of the aristotle dataset is valid."""
    dataset = load_dataset("aristotle")

    # Check for expected keys
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Check for keywords related to Aristotle
    text_content = ""
    # Check a few samples to find keywords
    keywords = ["virtue", "happiness", "political", "state", "city", "soul", "nature", "good"]
    found_keyword = False

    # Iterate through a few samples (slice returns dict of lists)
    samples = dataset[:20]
    for text in samples["text"]:
        if any(keyword in text.lower() for keyword in keywords):
            found_keyword = True
            break

    assert found_keyword, "Did not find expected keywords in the first 20 samples."

def test_aristotle_negative_assertions():
    """Test that the dataset does not contain unwanted artifacts."""
    dataset = load_dataset("aristotle")

    # Check for Gutenberg artifacts
    unwanted_phrases = [
        "Project Gutenberg",
        "START OF THE PROJECT",
        "END OF THE PROJECT",
        "Distributed Proofreaders"
    ]

    samples = dataset[:50]
    for text in samples["text"]:
        for phrase in unwanted_phrases:
            assert phrase not in text, f"Found unwanted phrase: {phrase}"

def test_aristotle_metadata():
    """Test that the metadata is correct."""
    metadata_path = get_abs_path("../socials_data/personalities/aristotle/metadata.json")
    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    assert metadata["id"] == "aristotle"
    assert metadata["name"] == "Aristotle"
    assert len(metadata["sources"]) == 4

    source_titles = [s["title"] for s in metadata["sources"]]
    assert "The Nicomachean Ethics" in source_titles
    assert "Politics" in source_titles
    assert "The Poetics" in source_titles
    assert "The Categories" in source_titles
