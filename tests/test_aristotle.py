import pytest
from socials_data.core.loader import load_dataset
import os
import json

PERSONALITY_ID = "aristotle"

def test_aristotle_dataset_exists():
    """Test that the aristotle dataset can be loaded."""
    try:
        ds = load_dataset(PERSONALITY_ID)
    except Exception as e:
        pytest.fail(f"Failed to load dataset: {e}")

    assert ds is not None
    assert len(ds) > 100 # Should be plenty of chunks

    # Check sample
    sample = ds[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

def test_aristotle_content():
    """Test specific content exists in the dataset."""
    ds = load_dataset(PERSONALITY_ID)

    # We expect terms like "virtue", "happiness", "state", "tragedy"
    found_virtue = False
    found_state = False

    # Iterate a subset to save time if needed, but for unit tests full scan is okay if small
    # or just check until found
    for item in ds:
        text = item["text"].lower()
        if "virtue" in text:
            found_virtue = True
        if "state" in text:
            found_state = True
        if found_virtue and found_state:
            break

    assert found_virtue, "Could not find 'virtue' in Aristotle dataset"
    assert found_state, "Could not find 'state' in Aristotle dataset"

def test_metadata_structure():
    """Verify metadata.json structure."""
    metadata_path = f"socials_data/personalities/{PERSONALITY_ID}/metadata.json"
    assert os.path.exists(metadata_path)

    with open(metadata_path, 'r') as f:
        data = json.load(f)

    assert data['id'] == PERSONALITY_ID
    assert "system_prompt" in data
    assert len(data['sources']) == 3
    assert data['sources'][0]['title'] == "Politics"
