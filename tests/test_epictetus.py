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
    # source could be enchiridion.txt or discourses.txt
    assert sample["source"] in ["enchiridion.txt", "discourses.txt"]

def test_epictetus_content_keywords():
    """Test that the content contains expected keywords."""
    dataset = load_dataset("epictetus")

    found_stoic_concept = False
    found_control = False

    # Check all samples (dataset is small)
    for sample in dataset:
        text = sample["text"].lower()
        if any(w in text for w in ["control", "power", "up to us", "prohairesis"]):
            found_control = True
        if any(w in text for w in ["god", "zeus", "nature", "will", "judgment"]):
            found_stoic_concept = True

    assert found_control, "Did not find control/power concepts"
    assert found_stoic_concept, "Did not find Stoic concepts"

def test_epictetus_metadata():
    """Verify metadata file exists and is valid."""
    metadata_path = Path("socials_data/personalities/epictetus/metadata.json")
    assert metadata_path.exists()

    with open(metadata_path, "r") as f:
        data = json.load(f)

    assert data["id"] == "epictetus"
    assert "Stoic" in data["system_prompt"]
    assert "control" in data["system_prompt"]
