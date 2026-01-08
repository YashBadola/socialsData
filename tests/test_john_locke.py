import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_john_locke_dataset_loads():
    """Verify that the John Locke dataset loads correctly and contains valid data."""
    dataset = load_dataset("john_locke")

    assert len(dataset) > 0, "Dataset should not be empty"

    # Check column names
    assert "text" in dataset.column_names
    assert "source" in dataset.column_names

    # Check content of a sample
    sample = dataset[0]
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0
    assert sample["source"] in [
        "second_treatise.txt",
        "essay_human_understanding_vol1.txt",
        "essay_human_understanding_vol2.txt"
    ]

def test_john_locke_metadata():
    """Verify metadata integrity for John Locke."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("john_locke")

    assert metadata["name"] == "John Locke"
    assert "Father of Liberalism" in metadata["description"] or "Father of Liberalism" in metadata["system_prompt"]
    assert len(metadata["sources"]) == 3
