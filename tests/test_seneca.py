import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager
from pathlib import Path

def test_load_seneca_dataset():
    """Test that the Seneca dataset can be loaded."""
    dataset = load_dataset("seneca")
    assert len(dataset) > 0
    # Check that the first item has the expected structure
    first_item = dataset[0]
    assert "text" in first_item
    assert "source" in first_item
    # Check for keywords that would likely appear in the text
    # "Stoic", "virtue", "Lucilius", "nature"
    # Note: text is chunked, so we might need to check a few samples or just general content.

    # Let's verify at least one sample contains "virtue" or "happy" or "life"
    found_keyword = False
    for item in dataset:
        text = item["text"].lower()
        if "virtue" in text or "happy" in text or "life" in text:
            found_keyword = True
            break
    assert found_keyword, "Dataset should contain relevant keywords"

def test_seneca_metadata():
    """Test that Seneca metadata is correct."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("seneca")
    assert metadata["name"] == "Lucius Annaeus Seneca"
    assert metadata["id"] == "seneca"
    assert "Stoic" in metadata["system_prompt"]
