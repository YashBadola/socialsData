import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager
import os

def test_soren_kierkegaard_exists():
    pm = PersonalityManager()
    personalities = pm.list_personalities()
    assert "søren_kierkegaard" in personalities

def test_soren_kierkegaard_metadata():
    pm = PersonalityManager()
    metadata = pm.get_metadata("søren_kierkegaard")
    assert metadata["name"] == "Søren Kierkegaard"
    assert "existentialist" in metadata["description"]

def test_soren_kierkegaard_dataset_load():
    # Only verify we can load the text dataset since we didn't generate QA
    dataset = load_dataset("søren_kierkegaard")
    assert len(dataset) > 0
    assert "text" in dataset[0]
    assert "Either/Or" in dataset[0]["text"]
