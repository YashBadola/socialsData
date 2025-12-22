import pytest
from socials_data import load_dataset
from datasets import Dataset

def test_load_immanuel_kant():
    """Test loading the Immanuel Kant dataset."""
    dataset = load_dataset("immanuel_kant")

    assert isinstance(dataset, Dataset)
    assert len(dataset) > 0

    # Check sample content
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] == "critique_pure_reason.txt"

    # Check for keywords
    text = sample["text"].lower()
    # Note: the first chunk might be the preface or introduction, so these keywords might not appear immediately
    # if the chunks are small. But let's check a general term if the text is large enough.
    # The output from head -n 5 showed it contains a lot of text per chunk.
    # Let's check for "reason" which should be everywhere.
    assert "reason" in text or "critique" in text or "knowledge" in text

def test_metadata_completeness():
    """Test that metadata is correctly structured."""
    # Since we can't easily import the metadata file directly in test without reading it,
    # we rely on load_dataset which presumably uses it.
    # However, we can read the file to verify fields if we want.
    import json
    import pathlib

    metadata_path = pathlib.Path("socials_data/personalities/immanuel_kant/metadata.json")
    assert metadata_path.exists()

    with open(metadata_path, "r") as f:
        data = json.load(f)

    assert data["name"] == "Immanuel Kant"
    assert data["id"] == "immanuel_kant"
    assert "system_prompt" in data
    assert "sources" in data
    assert len(data["sources"]) > 0
