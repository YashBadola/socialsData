import pytest
from socials_data.core.manager import PersonalityManager
from socials_data.core.loader import load_dataset
from pathlib import Path

def test_plato_dataset_exists():
    """Test that the Plato dataset is correctly registered."""
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "plato" in personalities

def test_plato_metadata():
    """Test that Plato's metadata is correct."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("plato")
    assert metadata["name"] == "Plato"
    assert "Socrates" in metadata["system_prompt"]
    assert len(metadata["sources"]) == 5

def test_plato_data_content():
    """Test that the processed data contains expected content."""
    # We load the dataset directly using the loader
    # Since load_dataset might require HF structure or similar, we check file directly first
    # But let's try to use the loader if possible, or simulate it.

    # The load_dataset function in this repo likely wraps "datasets.load_dataset('json', ...)"
    # Let's inspect the loader code to be sure, but for now we can read the jsonl directly
    # to avoid complex mocking if not needed.

    dataset_path = Path("socials_data/personalities/plato/processed/data.jsonl")
    assert dataset_path.exists()

    import json
    with open(dataset_path, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0

    # Check a sample
    sample = json.loads(lines[0])
    assert "text" in sample
    assert "source" in sample
    assert len(sample["text"]) > 100

    # Check for keywords
    text_content = " ".join([json.loads(line)["text"] for line in lines[:10]])
    assert "Socrates" in text_content or "virtue" in text_content or "justice" in text_content

def test_load_dataset_integration():
    """Integration test with the load_dataset function."""
    # This requires the package to be installed and working
    try:
        ds = load_dataset("plato")
        assert len(ds) > 0
        assert "text" in ds.column_names
        assert "source" in ds.column_names
    except Exception as e:
        pytest.fail(f"Failed to load dataset: {e}")
