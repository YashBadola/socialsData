import os
import pytest
from socials_data.core.loader import load_dataset
from pathlib import Path
import json

def test_load_aristotle_dataset():
    """Test loading the Aristotle dataset."""
    dataset = load_dataset("aristotle")

    # Check if dataset is not empty
    assert len(dataset) > 0

    # Check format
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Verify content keywords
    # Nicomachean Ethics keywords
    ethics_found = any("virtue" in x["text"].lower() and "happiness" in x["text"].lower() for x in dataset)
    # Politics keywords
    politics_found = any("state" in x["text"].lower() and "constitution" in x["text"].lower() for x in dataset)
    # Poetics keywords
    poetics_found = any("tragedy" in x["text"].lower() or "imitation" in x["text"].lower() for x in dataset)
    # Categories keywords
    categories_found = any("substance" in x["text"].lower() or "predicate" in x["text"].lower() for x in dataset)

    assert ethics_found or politics_found or poetics_found or categories_found

def test_aristotle_metadata():
    """Verify metadata exists and is correct."""
    metadata_path = Path("socials_data/personalities/aristotle/metadata.json")
    assert metadata_path.exists()

    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    assert metadata["id"] == "aristotle"
    assert metadata["name"] == "Aristotle"
    assert "system_prompt" in metadata
    assert len(metadata["sources"]) == 4

def test_raw_files_exist():
    """Verify raw files were downloaded."""
    raw_dir = Path("socials_data/personalities/aristotle/raw")
    assert (raw_dir / "nicomachean_ethics.txt").exists()
    assert (raw_dir / "politics.txt").exists()
    assert (raw_dir / "poetics.txt").exists()
    assert (raw_dir / "categories.txt").exists()

def test_no_gutenberg_headers():
    """Check that Gutenberg headers are largely removed."""
    # This is a heuristic check
    dataset = load_dataset("aristotle")

    for item in dataset:
        text = item["text"]
        # Basic check for common Gutenberg boilerplate that should have been stripped
        assert "*** START OF THE PROJECT GUTENBERG" not in text
        assert "*** END OF THE PROJECT GUTENBERG" not in text
