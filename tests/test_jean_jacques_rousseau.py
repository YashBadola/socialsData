import os
import json
import pytest
from socials_data.core.loader import load_dataset

PERSONALITY_ID = "jean_jacques_rousseau"

def test_dataset_exists():
    """Test that the personality directory exists and has the expected structure."""
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../socials_data/personalities", PERSONALITY_ID)
    assert os.path.exists(base_dir)
    assert os.path.exists(os.path.join(base_dir, "metadata.json"))
    assert os.path.exists(os.path.join(base_dir, "raw"))
    assert os.path.exists(os.path.join(base_dir, "processed"))
    assert os.path.exists(os.path.join(base_dir, "processed", "data.jsonl"))

def test_load_dataset():
    """Test that the dataset can be loaded using the library function."""
    dataset = load_dataset(PERSONALITY_ID)
    assert dataset is not None
    # We expect at least some samples
    assert len(dataset) > 100

    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

def test_content_integrity():
    """Test that specific keywords and content appear in the dataset."""
    dataset = load_dataset(PERSONALITY_ID)

    # Check for keywords related to Rousseau
    keywords = ["Social Contract", "Emile", "confessions", "liberty", "nature", "inequality"]
    found_keywords = {k: False for k in keywords}

    # Check a subset of samples to be efficient
    for i in range(min(len(dataset), 500)):
        text = dataset[i]["text"]
        for k in keywords:
            if k.lower() in text.lower():
                found_keywords[k] = True

    # We might not find 'Social Contract' explicitly in the text if it's chunks,
    # but we should find 'nature' or 'liberty'
    assert found_keywords["nature"] or found_keywords["liberty"]

def test_no_license_artifacts():
    """Test that Project Gutenberg license text is not present."""
    dataset = load_dataset(PERSONALITY_ID)

    # Check for common license phrases
    license_phrases = [
        "Project Gutenberg License",
        "START OF THE PROJECT GUTENBERG",
        "END OF THE PROJECT GUTENBERG",
        "Call to action", # sometimes in footer
        "Donate to Project Gutenberg"
    ]

    for i in range(len(dataset)):
        text = dataset[i]["text"]
        for phrase in license_phrases:
            assert phrase not in text, f"Found license artifact '{phrase}' in sample {i}"

def test_metadata():
    """Test that metadata is correct."""
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../socials_data/personalities", PERSONALITY_ID)
    with open(os.path.join(base_dir, "metadata.json"), "r") as f:
        meta = json.load(f)

    assert meta["id"] == PERSONALITY_ID
    assert meta["name"] == "Jean-Jacques Rousseau"
    assert "system_prompt" in meta
    assert len(meta["sources"]) == 3
