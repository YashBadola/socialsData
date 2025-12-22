import pytest
from socials_data.core.loader import load_dataset
from pathlib import Path
import json

def test_load_seneca_dataset():
    # Load the dataset
    ds = load_dataset("seneca")

    # Check if dataset is not empty
    assert len(ds) > 0

    # Check a sample entry
    sample = ds[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 10

    # Check for content relevance
    full_text = " ".join([entry["text"] for entry in ds])
    keywords = ["virtue", "anger", "benefit", "nature", "happy life", "stoic"]
    found_keywords = [kw for kw in keywords if kw in full_text.lower()]
    assert len(found_keywords) > 0, f"Expected to find Seneca keywords, but found none in: {full_text[:500]}..."

    # Verify we don't have the Turgenev text
    assert "turgenev" not in full_text.lower()
    assert "sportsman's sketches" not in full_text.lower()

    # Verify no Gutenberg headers
    assert "START OF THE PROJECT GUTENBERG EBOOK" not in full_text

def test_seneca_processed_file_exists():
    path = Path("socials_data/personalities/seneca/processed/data.jsonl")
    assert path.exists()

    with open(path, "r") as f:
        lines = f.readlines()
        assert len(lines) > 0
