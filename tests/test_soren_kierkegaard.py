import json
from pathlib import Path
from socials_data import load_dataset
import pytest

def test_kierkegaard_dataset_loads():
    """Test that the Kierkegaard dataset can be loaded via the loader."""
    dataset = load_dataset("soren_kierkegaard")
    assert len(dataset) > 0

    # Check a sample
    sample = dataset[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0
    assert "source" in sample
    # One of the sources should be present
    assert any(x in sample["source"] for x in ["fear_and_trembling_excerpt.txt", "sickness_unto_death_excerpt.txt"])

def test_kierkegaard_content_keywords():
    """Test that the content contains expected keywords."""
    dataset = load_dataset("soren_kierkegaard")

    found_faith = False
    found_self = False

    # Check samples
    for i in range(len(dataset)):
        text = dataset[i]["text"].lower()
        if "faith" in text and "paradox" in text:
            found_faith = True
        if "spirit" in text and "self" in text:
            found_self = True

    assert found_faith, "Did not find faith/paradox concepts"
    assert found_self, "Did not find spirit/self concepts"

def test_kierkegaard_metadata():
    """Verify metadata file exists and is valid."""
    metadata_path = Path("socials_data/personalities/soren_kierkegaard/metadata.json")
    assert metadata_path.exists()

    with open(metadata_path, "r") as f:
        data = json.load(f)

    assert data["id"] == "soren_kierkegaard"
    assert "Existentialism" in data["system_prompt"]
