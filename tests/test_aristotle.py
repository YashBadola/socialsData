import json
from pathlib import Path
import pytest
from socials_data import load_dataset

def test_aristotle_dataset_loading():
    """Test that the Aristotle dataset loads correctly."""
    dataset = load_dataset("aristotle")
    assert len(dataset) > 0

    # Check basic schema
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Verify content
    text = sample["text"]
    assert isinstance(text, str)
    assert len(text) > 0

def test_aristotle_content_verification():
    """Verify that specific Aristotle texts are present."""
    dataset = load_dataset("aristotle")

    # We expect content from Ethics, Politics, Poetics
    found_ethics = False
    found_politics = False
    found_poetics = False

    for item in dataset:
        src = item["source"]
        if "nicomachean_ethics" in src:
            found_ethics = True
        elif "politics" in src:
            found_politics = True
        elif "poetics" in src:
            found_poetics = True

        if found_ethics and found_politics and found_poetics:
            break

    assert found_ethics, "Nicomachean Ethics content not found"
    assert found_politics, "Politics content not found"
    assert found_poetics, "Poetics content not found"

def test_metadata_completeness():
    """Test that metadata.json has all required fields."""
    import json
    metadata_path = Path("socials_data/personalities/aristotle/metadata.json")
    assert metadata_path.exists()

    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    assert metadata["id"] == "aristotle"
    assert "Aristotle" in metadata["name"]
    assert "system_prompt" in metadata
    assert len(metadata["sources"]) == 3
