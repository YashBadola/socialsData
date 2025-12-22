import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager
import json

def test_seneca_dataset_structure():
    # Load dataset
    ds = load_dataset("seneca")
    assert len(ds) > 0

    # Check first sample
    sample = ds[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

def test_seneca_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("seneca")
    assert metadata["name"] == "Seneca"
    assert "Stoic" in metadata["system_prompt"]
    assert len(metadata["sources"]) > 0
