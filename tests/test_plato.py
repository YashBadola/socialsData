import os
import pytest
from socials_data.core.loader import load_dataset
from pathlib import Path
import json

def test_plato_dataset_exists():
    """Test that the Plato dataset can be loaded."""
    # Ensure we are in the root directory for relative paths to work
    base_dir = Path(__file__).parent.parent

    # Check directory structure
    plato_dir = base_dir / "socials_data" / "personalities" / "plato"
    assert plato_dir.exists()
    assert (plato_dir / "metadata.json").exists()
    assert (plato_dir / "raw").exists()
    assert (plato_dir / "processed" / "data.jsonl").exists()

def test_plato_metadata():
    """Test metadata content for Plato."""
    base_dir = Path(__file__).parent.parent
    metadata_path = base_dir / "socials_data" / "personalities" / "plato" / "metadata.json"

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    assert metadata["id"] == "plato"
    assert metadata["name"] == "Plato"
    assert "Socrates" in metadata["system_prompt"]
    assert len(metadata["sources"]) == 4

def test_plato_data_content():
    """Test content of the processed data."""
    # We load the dataset using the library function
    # Note: Since load_dataset relies on 'datasets' and local paths,
    # we need to make sure it points to the right place.
    # The 'load_dataset' in socials_data.core.loader seems to be a wrapper or direct import.
    # Let's try to manually inspect the jsonl first to avoid library path issues in test environment if any.

    base_dir = Path(__file__).parent.parent
    data_path = base_dir / "socials_data" / "personalities" / "plato" / "processed" / "data.jsonl"

    with open(data_path, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0

    # Check a random sample
    sample = json.loads(lines[0])
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)

    # Check for keywords
    text_content = " ".join([json.loads(line)["text"] for line in lines])
    assert "Socrates" in text_content
    assert "Republic" in text_content or "justice" in text_content.lower()

def test_plato_no_gutenberg_headers():
    """Test that Gutenberg headers are largely removed."""
    base_dir = Path(__file__).parent.parent
    data_path = base_dir / "socials_data" / "personalities" / "plato" / "processed" / "data.jsonl"

    with open(data_path, "r") as f:
        for line in f:
            data = json.loads(line)
            text = data["text"]
            assert "START OF THE PROJECT GUTENBERG" not in text
            assert "END OF THE PROJECT GUTENBERG" not in text
