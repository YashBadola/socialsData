import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_soren_kierkegaard_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "soren_kierkegaard" in personalities

def test_soren_kierkegaard_load():
    dataset = load_dataset("soren_kierkegaard")
    assert dataset is not None
    assert len(dataset) > 0

    # Check if the first item has text
    item = dataset[0]
    assert "text" in item
    assert "Preface" in item["text"]
    assert "source" in item
    assert item["source"] == "excerpts.txt"
