
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager
import os

def test_soren_kierkegaard_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "soren_kierkegaard" in personalities

def test_soren_kierkegaard_dataset_structure():
    """
    Test that the dataset for Soren Kierkegaard can be loaded and has the correct structure.
    """
    try:
        dataset = load_dataset("soren_kierkegaard")
    except ValueError as e:
        pytest.fail(f"Failed to load dataset: {e}")

    # Check that it's a Dataset object (from Hugging Face datasets)
    from datasets import Dataset
    assert isinstance(dataset, Dataset)

    # Check if there is data
    assert len(dataset) > 0

    # Check columns
    assert "text" in dataset.column_names

    # Check content of a sample
    sample = dataset[0]
    assert isinstance(sample['text'], str)
    assert len(sample['text']) > 0

    # Verify that some known text is present in the dataset
    all_text = " ".join(dataset['text'])
    assert "Fear and Trembling" in all_text or "Either/Or" in all_text
