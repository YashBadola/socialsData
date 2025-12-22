
import pytest
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset
import os

def test_seneca_personality_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "seneca" in personalities

def test_seneca_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("seneca")
    assert metadata["name"] == "Lucius Annaeus Seneca"
    assert metadata["id"] == "seneca"
    assert "gutenberg.org" in metadata["sources"][0]["url"]

def test_seneca_dataset_loading():
    # Ensure processed data exists
    dataset = load_dataset("seneca")
    assert dataset is not None
    # We expect at least one sample
    assert len(dataset) > 0

    sample = dataset[0]
    assert "text" in sample
    # Check for some keyword likely to be in Seneca's text
    text = sample["text"]
    assert "Seneca" in text or "virtue" in text or "anger" in text or "clemency" in text

if __name__ == "__main__":
    pytest.main([__file__])
