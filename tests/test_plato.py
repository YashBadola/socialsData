import pytest
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset

def test_plato_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "plato" in personalities

def test_plato_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("plato")
    assert metadata["name"] == "Plato"
    assert "The Republic" in [s["title"] for s in metadata["sources"]]

def test_plato_load_dataset():
    # Load dataset
    ds = load_dataset("plato")
    assert len(ds) > 0

    # Check sample
    sample = ds[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Check for content specific to Plato
    # Since we have "The Republic", "Symposium", "Apology", we can search for common terms
    # across the dataset to verify coverage, or just pick one.
    # We'll just ensure at least one sample mentions 'Socrates' or 'dialogue' or typical words.
    found_socrates = False
    for item in ds:
        if "Socrates" in item["text"]:
            found_socrates = True
            break
    assert found_socrates, "Dataset should contain mentions of Socrates"
