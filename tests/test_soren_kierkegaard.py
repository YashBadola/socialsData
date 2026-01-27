import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_soren_kierkegaard_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "søren_kierkegaard" in personalities

def test_soren_kierkegaard_dataset():
    # This assumes the dataset has been processed
    dataset = load_dataset("søren_kierkegaard")
    assert len(dataset) > 0
    assert "text" in dataset[0]

    # Check for some characteristic text
    # Since we loaded the whole file as chunks (or one big chunk), we check the first one
    first_entry = dataset[0]['text']
    assert "Kierkegaard" in first_entry or "Selections" in first_entry
