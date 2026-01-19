from socials_data.core.loader import load_dataset
import pytest

def test_load_soren_kierkegaard_dataset():
    """Test loading the Søren Kierkegaard dataset."""
    dataset = load_dataset("søren_kierkegaard")

    # Check if dataset is not empty
    assert len(dataset) > 0

    # Check if dataset has expected columns
    assert "text" in dataset.features

    # Check for specific content from the excerpts
    found_quote = False
    for item in dataset:
        if "Anxiety is the dizziness of freedom" in item["text"]:
            found_quote = True
            break

    assert found_quote, "The famous quote about anxiety was not found in the dataset."

def test_soren_kierkegaard_metadata_structure():
    """Test if the metadata follows the correct structure."""
    import json
    import os

    metadata_path = "socials_data/personalities/søren_kierkegaard/metadata.json"
    assert os.path.exists(metadata_path)

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    required_fields = ["name", "id", "description", "system_prompt", "sources", "license"]
    for field in required_fields:
        assert field in metadata

    assert metadata["id"] == "søren_kierkegaard"
    assert "Søren Kierkegaard" in metadata["name"]
    assert len(metadata["sources"]) > 0
