import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager
from pathlib import Path

def test_kierkegaard_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "søren_kierkegaard" in personalities

def test_kierkegaard_dataset_loading():
    # Load the dataset for Søren Kierkegaard
    dataset = load_dataset("søren_kierkegaard")

    # Check if dataset is not empty
    assert len(dataset) > 0

    # Check for expected content in the text
    texts = [item['text'] for item in dataset]
    assert any("The Sickness Unto Death is despair" in text for text in texts)
    assert any("The Story of Abraham" in text for text in texts)
    assert any("The Journals of Søren Kierkegaard" in text for text in texts)
    assert any("Either/Or" in text for text in texts)

def test_kierkegaard_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("søren_kierkegaard")
    assert metadata['name'] == "Søren Kierkegaard"
    assert "existentialist" in metadata['description']
