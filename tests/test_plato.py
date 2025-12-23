import os
import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

def test_plato_exists():
    """Verify that Plato exists in the manager list."""
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "plato" in personalities

def test_plato_load_dataset():
    """Verify that the Plato dataset can be loaded."""
    # This might require PYTHONPATH to be set if running directly, but pytest handles it if configured.
    # However, load_dataset relies on 'datasets' loading local files.

    # Check if processed file exists first
    manager = PersonalityManager()
    dataset_path = manager.base_dir / "plato" / "processed" / "data.jsonl"
    assert dataset_path.exists(), "Processed data file missing"

    # Attempt load
    ds = load_dataset("plato")
    assert len(ds) > 0

    # Check schema
    sample = ds[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert isinstance(sample["source"], str)

    # Check content relevance (naive check)
    # The text is chunked, so we check if any chunk contains "Socrates" or "Republic"
    # But ds is a dataset object, iterating it works.

    found_keyword = False
    for item in ds:
        text = item["text"]
        if "Socrates" in text or "Republic" in text or "Plato" in text or "virtue" in text:
            found_keyword = True
            break
    assert found_keyword, "No relevant keywords found in the first samples."

def test_plato_metadata():
    """Verify metadata integrity."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("plato")
    assert metadata["name"] == "Plato"
    assert metadata["id"] == "plato"
    assert len(metadata["sources"]) == 3
