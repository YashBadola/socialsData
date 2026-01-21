import pytest
from socials_data.core.loader import load_dataset
import os

def test_soren_kierkegaard_dataset_loading():
    """Test that the Søren Kierkegaard dataset loads correctly."""
    dataset = load_dataset("soren_kierkegaard")

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check if entries have text and source
    for entry in dataset:
        assert 'text' in entry
        assert 'source' in entry
        assert len(entry['text']) > 0

def test_soren_kierkegaard_metadata():
    """Test that the metadata exists and is correct."""
    metadata_path = "socials_data/personalities/soren_kierkegaard/metadata.json"
    assert os.path.exists(metadata_path)

    # We could load and check specific fields if needed
    import json
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    assert metadata['name'] == "Søren Kierkegaard"
    assert metadata['id'] == "soren_kierkegaard"

def test_soren_kierkegaard_files_exist():
    """Test that the raw and processed files exist."""
    raw_path = "socials_data/personalities/soren_kierkegaard/raw"
    processed_path = "socials_data/personalities/soren_kierkegaard/processed/data.jsonl"

    assert os.path.exists(raw_path)
    assert os.path.exists(processed_path)

    # Check if raw files exist
    assert os.path.exists(os.path.join(raw_path, "fear_and_trembling_excerpt.txt"))
    assert os.path.exists(os.path.join(raw_path, "either_or_diapsalmata.txt"))
