import os
import json
import pytest
from socials_data.core.loader import load_dataset

PERSONALITY_ID = "jean_jacques_rousseau"

def test_load_rousseau_dataset():
    """Test loading the Rousseau dataset."""
    try:
        dataset = load_dataset(PERSONALITY_ID)
    except ValueError as e:
        pytest.fail(f"Failed to load dataset: {e}")

    # Check that it returns a Hugging Face Dataset
    assert dataset is not None
    assert len(dataset) > 0

    # Check first item structure
    first_item = dataset[0]
    assert "text" in first_item
    assert "source" in first_item
    assert isinstance(first_item["text"], str)
    assert len(first_item["text"]) > 0

    # Verify content relevance (basic check)
    # Search for a few keywords across a sample of texts to ensure we have the right content
    sample_texts = dataset[:100]["text"] # Get first 100 chunks
    combined_text = " ".join(sample_texts).lower()

    keywords = ["inequality", "nature", "contract", "liberty", "education", "man"]
    found_keywords = [k for k in keywords if k in combined_text]

    # We expect to find at least some of these keywords
    assert len(found_keywords) > 0, f"None of the expected keywords {keywords} found in sample text."

def test_metadata_integrity():
    """Test that the metadata file is correct."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    metadata_path = os.path.join(base_dir, "socials_data", "personalities", PERSONALITY_ID, "metadata.json")

    assert os.path.exists(metadata_path)

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    assert metadata["id"] == PERSONALITY_ID
    assert "Jean-Jacques Rousseau" in metadata["name"]
    assert len(metadata["sources"]) == 4
    assert "system_prompt" in metadata
    assert "Public Domain" in metadata["license"]

def test_no_gutenberg_artifacts():
    """Test that Gutenberg headers/footers are cleaned."""
    dataset = load_dataset(PERSONALITY_ID)

    # Check a large sample or all for artifacts
    # Checking for common artifacts
    artifacts = [
        "*** START OF THE PROJECT GUTENBERG",
        "*** END OF THE PROJECT GUTENBERG",
        "Project Gutenberg eBook",
    ]

    for item in dataset:
        text = item["text"]
        for artifact in artifacts:
            assert artifact not in text, f"Found artifact '{artifact}' in text."
