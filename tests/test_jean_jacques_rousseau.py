
import os
import pytest
from socials_data.core.manager import PersonalityManager
from socials_data.core.loader import load_dataset

@pytest.fixture
def personality_manager():
    return PersonalityManager()

def test_rousseau_personality_exists(personality_manager):
    """Test that Jean-Jacques Rousseau personality is correctly registered."""
    personalities = personality_manager.list_personalities()
    assert "jean_jacques_rousseau" in personalities

def test_rousseau_metadata(personality_manager):
    """Test that metadata for Rousseau is correct."""
    metadata = personality_manager.get_metadata("jean_jacques_rousseau")
    assert metadata["name"] == "Jean-Jacques Rousseau"
    assert "Enlightenment" in metadata["system_prompt"]
    assert "nature" in metadata["system_prompt"]
    assert len(metadata["sources"]) == 4

def test_rousseau_raw_files_exist():
    """Test that raw files were downloaded."""
    base_path = os.path.join("socials_data", "personalities", "jean_jacques_rousseau", "raw")
    expected_files = [
        "the_social_contract.txt",
        "emile.txt",
        "the_confessions.txt",
        "discourse_on_inequality.txt"
    ]
    for filename in expected_files:
        assert os.path.exists(os.path.join(base_path, filename))

def test_rousseau_dataset_loading():
    """Test that the dataset can be loaded and contains valid data."""
    dataset = load_dataset("jean_jacques_rousseau")

    # Check that we have data
    assert len(dataset) > 0

    # Check a sample
    sample = dataset[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100

    # Check for specific content (keywords likely to appear)
    # We check the whole dataset for keywords to be sure
    text_content = "".join(dataset["text"])
    assert "nature" in text_content.lower()
    assert "contract" in text_content.lower()

    # Negative assertions - check for Gutenberg license which should be cleaned
    assert "Project Gutenberg License" not in text_content
    assert "START OF THE PROJECT" not in text_content
