import os
import json
import pytest
from socials_data.core.loader import load_dataset

PERSONALITY_ID = "jean_jacques_rousseau"

def test_personality_exists():
    """Verify that the personality directory and metadata exist."""
    base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "socials_data", "personalities")
    personality_dir = os.path.join(base_dir, PERSONALITY_ID)
    metadata_path = os.path.join(personality_dir, "metadata.json")

    assert os.path.isdir(personality_dir), f"Directory for {PERSONALITY_ID} not found."
    assert os.path.isfile(metadata_path), f"Metadata file for {PERSONALITY_ID} not found."

def test_load_dataset():
    """Verify that the dataset loads using the package loader."""
    ds = load_dataset(PERSONALITY_ID)
    assert len(ds) > 0, "Dataset should not be empty."

    # Check first item structure
    item = ds[0]
    assert "text" in item
    assert "source" in item
    assert isinstance(item["text"], str)
    assert len(item["text"]) > 0

def test_content_relevance():
    """Check for specific keywords relevant to Rousseau in the dataset."""
    ds = load_dataset(PERSONALITY_ID)

    keywords = ["Social Contract", "Emile", "Confessions", "inequality", "freedom"]
    found = {kw: False for kw in keywords}

    # Sample a few entries to avoid scanning everything if not needed,
    # but scanning all is safer for a test suite.
    for item in ds:
        text = item["text"]
        for kw in keywords:
            if kw in text:
                found[kw] = True

    # We might not find *all* keywords in every chunk, but we should find some.
    # Actually, "Social Contract" might be in the title or text.
    assert found["freedom"] or found["inequality"], "Dataset should contain core themes like freedom or inequality."

def test_no_gutenberg_headers():
    """Ensure that Project Gutenberg boilerplate is removed."""
    ds = load_dataset(PERSONALITY_ID)

    markers = [
        "Project Gutenberg License",
        "START OF THE PROJECT GUTENBERG",
        "END OF THE PROJECT GUTENBERG"
    ]

    for item in ds:
        text = item["text"]
        for marker in markers:
            assert marker not in text, f"Found Gutenberg marker '{marker}' in text source {item['source']}"
