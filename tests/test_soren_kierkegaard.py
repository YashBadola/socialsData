import pytest
from socials_data.core.loader import load_dataset
import os

def test_load_dataset_soren_kierkegaard():
    """
    Test that the dataset for Sören Kierkegaard can be loaded and contains valid data.
    """
    try:
        dataset = load_dataset("soren_kierkegaard")
    except Exception as e:
        pytest.fail(f"Failed to load dataset: {e}")

    assert dataset is not None
    assert len(dataset) > 0

    # Check if the first entry has the expected structure
    first_entry = dataset[0]
    assert "text" in first_entry
    assert isinstance(first_entry["text"], str)
    assert len(first_entry["text"]) > 0

def test_metadata_existence():
    """
    Test that the metadata file exists for Sören Kierkegaard.
    """
    metadata_path = "socials_data/personalities/soren_kierkegaard/metadata.json"
    assert os.path.exists(metadata_path)

def test_processed_data_existence():
    """
    Test that the processed data file exists for Sören Kierkegaard.
    """
    processed_path = "socials_data/personalities/soren_kierkegaard/processed/data.jsonl"
    assert os.path.exists(processed_path)
