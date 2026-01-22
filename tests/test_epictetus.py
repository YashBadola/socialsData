import json
from pathlib import Path
from socials_data.core.loader import load_dataset
import pytest

def test_epictetus_dataset_loads():
    """Test that the Epictetus dataset can be loaded via the loader."""
    dataset = load_dataset("epictetus")
    assert len(dataset) > 0

    # Check a sample
    sample = dataset[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0
    assert "source" in sample
    assert "discourses_excerpts.txt" in sample["source"] or "enchiridion_excerpts.txt" in sample["source"]

def test_epictetus_content_keywords():
    """Test that the content contains expected keywords."""
    dataset = load_dataset("epictetus")

    found_stoic_concept = False

    # Check all samples
    for item in dataset:
        text = item["text"].lower()
        if any(w in text for w in ["control", "opinion", "desire", "aversion", "nature", "will", "mind"]):
            found_stoic_concept = True
            break

    assert found_stoic_concept, "Did not find Stoic concepts in the dataset"

def test_epictetus_metadata():
    """Verify metadata file exists and is valid."""
    metadata_path = Path("socials_data/personalities/epictetus/metadata.json")
    assert metadata_path.exists()

    with open(metadata_path, "r") as f:
        data = json.load(f)

    assert data["id"] == "epictetus"
    assert "Stoic" in data["system_prompt"]
    assert "slave" in data["system_prompt"]
