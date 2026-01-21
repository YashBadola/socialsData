import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_jean_jacques_rousseau_exists():
    pm = PersonalityManager()
    personalities = pm.list_personalities()
    assert "jean_jacques_rousseau" in personalities

def test_jean_jacques_rousseau_dataset_loads():
    ds = load_dataset("jean_jacques_rousseau")
    assert len(ds) > 0
    assert "text" in ds[0]
    assert "born free" in ds[0]["text"]  # Check for key phrase
