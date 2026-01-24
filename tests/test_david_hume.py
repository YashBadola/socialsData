
import pytest
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset
import os

def test_david_hume_dataset_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "david_hume" in personalities

    metadata = manager.get_metadata("david_hume")
    assert metadata["name"] == "David Hume"
    assert metadata["id"] == "david_hume"

def test_load_david_hume_dataset():
    # Test loading the dataset
    # We expect it to return a Hugging Face Dataset object
    try:
        ds = load_dataset("david_hume")
    except ImportError:
        pytest.skip("datasets library not installed or configured correctly")

    assert len(ds) > 0
    sample = ds[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert "David Hume" in sample["text"] or "Understanding" in sample["text"] or "philosophy" in sample["text"] or len(sample["text"]) > 0

def test_david_hume_content():
    manager = PersonalityManager()
    path = manager.base_dir / "david_hume" / "processed" / "data.jsonl"
    assert path.exists()

    # Read first few lines to verify content
    with open(path, "r") as f:
        line = f.readline()
        assert "text" in line
        assert "source" in line
