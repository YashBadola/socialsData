import pytest
import os
from pathlib import Path
from socials_data import load_dataset
import json

PERSONALITY_ID = "aristotle"

def test_aristotle_exists():
    """Check if the personality directory and metadata exist."""
    base_dir = Path("socials_data/personalities") / PERSONALITY_ID
    assert base_dir.exists(), f"{PERSONALITY_ID} directory missing"
    assert (base_dir / "metadata.json").exists(), "metadata.json missing"
    assert (base_dir / "raw").exists(), "raw directory missing"
    assert (base_dir / "processed").exists(), "processed directory missing"

def test_metadata_content():
    """Verify metadata.json content."""
    base_dir = Path("socials_data/personalities") / PERSONALITY_ID
    with open(base_dir / "metadata.json", "r") as f:
        meta = json.load(f)

    assert meta["id"] == PERSONALITY_ID
    assert meta["name"] == "Aristotle"
    assert "system_prompt" in meta
    assert len(meta["sources"]) == 4

def test_raw_files_exist():
    """Verify raw files were downloaded."""
    raw_dir = Path("socials_data/personalities") / PERSONALITY_ID / "raw"
    expected_files = [
        "nicomachean_ethics.txt",
        "politics.txt",
        "poetics.txt",
        "categories.txt"
    ]
    for filename in expected_files:
        assert (raw_dir / filename).exists(), f"{filename} missing in raw/"

def test_load_dataset_works():
    """Verify the dataset can be loaded via HuggingFace datasets."""
    # This requires the 'processed/data.jsonl' to be valid
    ds = load_dataset(PERSONALITY_ID)
    assert len(ds) > 0

    # Check sample content
    sample = ds[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

def test_content_cleaning():
    """Verify that the standard Gutenberg headers are removed."""
    raw_dir = Path("socials_data/personalities") / PERSONALITY_ID / "raw"

    # Check one file for Gutenberg markers
    with open(raw_dir / "nicomachean_ethics.txt", "r", encoding="utf-8") as f:
        content = f.read()

    assert "*** START OF THE PROJECT GUTENBERG EBOOK" not in content
    assert "*** END OF THE PROJECT GUTENBERG EBOOK" not in content

    # Check that we have the specific start
    assert content.strip().startswith("Every art, and every science")
