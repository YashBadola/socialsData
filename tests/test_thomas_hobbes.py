import os
import json
import pytest
from socials_data.core.loader import load_dataset

def test_thomas_hobbes_exists():
    """Test that the Thomas Hobbes personality exists and metadata is correct."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    metadata_path = os.path.join(base_dir, "socials_data", "personalities", "thomas_hobbes", "metadata.json")

    assert os.path.exists(metadata_path), "Metadata file does not exist"

    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    assert metadata['id'] == "thomas_hobbes"
    assert metadata['name'] == "Thomas Hobbes"
    assert "Leviathan" in metadata['description']

def test_load_thomas_hobbes_dataset():
    """Test loading the Thomas Hobbes dataset."""
    dataset = load_dataset("thomas_hobbes")
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check first item
    item = dataset[0]
    assert "text" in item
    assert "source" in item
    assert item["source"] == "leviathan.txt"

    # Check for specific content
    text = item["text"]
    assert "Leviathan" in text or "LEVIATHAN" in text
    assert "Commonwealth" in text or "Common-wealth" in text

    # Check that Gutenberg headers are removed (negative assertion)
    assert "START OF THE PROJECT GUTENBERG" not in text
    assert "Project Gutenberg License" not in text
