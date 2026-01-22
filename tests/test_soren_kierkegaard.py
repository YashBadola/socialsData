import json
from pathlib import Path
from socials_data.core.loader import load_dataset

def test_metadata_soren_kierkegaard():
    """Test metadata for Søren Kierkegaard."""
    metadata_path = Path("socials_data/personalities/soren_kierkegaard/metadata.json")
    assert metadata_path.exists()

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    assert metadata["name"] == "Søren Kierkegaard"
    assert metadata["id"] == "soren_kierkegaard"
    assert "system_prompt" in metadata
    assert "subjectivity" in metadata["system_prompt"].lower() or "faith" in metadata["system_prompt"].lower()

def test_load_dataset_soren_kierkegaard():
    """Test loading the Søren Kierkegaard dataset."""
    dataset = load_dataset("soren_kierkegaard")
    assert len(dataset) > 0, "Dataset should not be empty"

    item = dataset[0]
    assert "text" in item
    assert "Faith is precisely this paradox" in item["text"]
