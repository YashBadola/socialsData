import os
import json
import pytest
from pathlib import Path
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

PERSONALITY_ID = "aristotle"

def test_metadata_exists():
    """Test that metadata.json exists and contains correct fields."""
    manager = PersonalityManager()
    metadata = manager.get_metadata(PERSONALITY_ID)

    assert metadata["id"] == PERSONALITY_ID
    assert metadata["name"] == "Aristotle"
    assert "system_prompt" in metadata
    assert len(metadata["sources"]) == 4

def test_raw_files_exist():
    """Test that raw files were downloaded."""
    base_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent
    raw_dir = base_dir / "socials_data" / "personalities" / PERSONALITY_ID / "raw"

    expected_files = ["nicomachean_ethics.txt", "politics.txt", "poetics.txt", "categories.txt"]
    for filename in expected_files:
        assert (raw_dir / filename).exists(), f"{filename} missing in raw directory"

def test_processed_data_content():
    """Test that processed data contains expected text and sources."""
    dataset = load_dataset(PERSONALITY_ID)

    # Check we have data
    assert len(dataset) > 0

    # Check sources
    sources = set(dataset["source"])
    expected_sources = {"nicomachean_ethics.txt", "politics.txt", "poetics.txt", "categories.txt"}
    assert sources == expected_sources

    # Check content in samples
    text_content = " ".join(dataset["text"][:10])

    # Keywords likely to be found in Aristotle's works
    keywords = ["virtue", "political", "state", "imitation", "substance", "category"]
    found_keywords = [k for k in keywords if k in text_content.lower()]
    assert len(found_keywords) > 0, "No expected keywords found in the dataset"

def test_no_license_text():
    """Ensure Project Gutenberg license text is removed."""
    dataset = load_dataset(PERSONALITY_ID)
    for text in dataset["text"]:
        assert "Project Gutenberg License" not in text
        assert "START OF THE PROJECT" not in text
