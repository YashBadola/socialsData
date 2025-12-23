import json
import pytest
from socials_data import load_dataset
from pathlib import Path

PERSONALITY_ID = "niccolo_machiavelli"

def test_load_dataset():
    """Test that the dataset loads correctly."""
    ds = load_dataset(PERSONALITY_ID)
    assert len(ds) > 0
    assert "text" in ds.column_names
    assert "source" in ds.column_names

def test_content_quality():
    """Test that the content contains expected keywords."""
    ds = load_dataset(PERSONALITY_ID)

    # Check for keywords related to Machiavelli
    keywords = ["prince", "state", "virtue", "fortune", "arms", "republic", "rome"]
    found_keywords = {k: False for k in keywords}

    # Check a sample of entries
    # We use a loop to check the first few entries, or until we find all keywords
    # Note: Dataset indexing might return a dict of lists if sliced, or a dict if single index
    # But when iterating, it yields rows.

    count = 0
    for row in ds:
        text = row["text"].lower()
        for k in keywords:
            if k in text:
                found_keywords[k] = True
        count += 1
        if count > 100: # Check first 100 chunks
            break

    # We don't expect *every* chunk to have these, but collectively they should appear.
    # Let's assert that at least some were found.
    assert found_keywords["prince"], "Keyword 'prince' not found in first 100 chunks"
    assert found_keywords["state"], "Keyword 'state' not found in first 100 chunks"

def test_metadata_structure():
    """Verify metadata.json structure."""
    import json
    path = Path(f"socials_data/personalities/{PERSONALITY_ID}/metadata.json")
    with open(path, "r") as f:
        meta = json.load(f)

    assert meta["id"] == PERSONALITY_ID
    assert "system_prompt" in meta
    assert len(meta["sources"]) == 3
