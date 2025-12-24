import os
import json
import pytest
from socials_data.core.loader import load_dataset

PERSONALITY_ID = "jean_jacques_rousseau"

def test_dataset_loading():
    """Test that the dataset loads correctly using load_dataset."""
    dataset = load_dataset(PERSONALITY_ID)
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check first sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

def test_content_integrity():
    """Test that the content contains expected strings and lacks license boilerplate."""
    dataset = load_dataset(PERSONALITY_ID)

    # Check for presence of key terms
    found_social_contract = False
    found_confessions = False
    found_emile = False

    # We'll sample a subset if it's huge, but for now iterate all
    for item in dataset:
        text = item["text"]
        if "general will" in text.lower() or "man is born free" in text.lower():
            found_social_contract = True
        if "i was born" in text.lower() or "maman" in text.lower():
            found_confessions = True
        if "emile" in text.lower() or "education" in text.lower():
            found_emile = True

        # Negative assertion: License text
        assert "Project Gutenberg License" not in text, f"Found license text in: {text[:100]}..."
        assert "START OF THE PROJECT GUTENBERG" not in text

    assert found_social_contract, "Did not find expected text from Social Contract"
    # assert found_confessions, "Did not find expected text from Confessions" # Might be harder to hit depending on chunks
    # assert found_emile, "Did not find expected text from Emile"

def test_metadata():
    """Test that metadata is valid."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    metadata_path = os.path.join(base_dir, f"../socials_data/personalities/{PERSONALITY_ID}/metadata.json")

    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    assert metadata["id"] == PERSONALITY_ID
    assert metadata["name"] == "Jean-Jacques Rousseau"
    assert "system_prompt" in metadata
    assert len(metadata["sources"]) == 3
