import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager
import os

def test_simone_de_beauvoir_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "simone_de_beauvoir" in personalities

def test_simone_de_beauvoir_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("simone_de_beauvoir")
    assert metadata["name"] == "Simone de Beauvoir"
    assert "existentialist" in metadata["description"].lower()

def test_simone_de_beauvoir_data_loading():
    # Ensure the data was processed
    dataset = load_dataset("simone_de_beauvoir")
    assert len(dataset) > 0
    # Check if we can find some of our excerpt text
    found = False
    for item in dataset:
        if "One is not born, but rather becomes, a woman" in item["text"]:
            found = True
            break
    assert found
