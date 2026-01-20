import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager
import os

def test_kierkegaard_exists():
    pm = PersonalityManager()
    personalities = pm.list_personalities()
    assert "søren_kierkegaard" in personalities

def test_kierkegaard_data_loading():
    dataset = load_dataset("søren_kierkegaard")
    assert dataset is not None
    assert len(dataset) > 0

    # Check if content matches what we expect
    first_entry = dataset[0]
    assert "text" in first_entry
    assert "source" in first_entry

    # Check for some specific text we added
    all_text = " ".join([entry['text'] for entry in dataset])
    assert "Anxiety is the dizziness of freedom" in all_text
    assert "Life can only be understood backwards" in all_text

def test_kierkegaard_metadata():
    pm = PersonalityManager()
    metadata = pm.get_metadata("søren_kierkegaard")
    assert metadata["name"] == "Søren Kierkegaard"
    assert "existentialist" in metadata["description"]
