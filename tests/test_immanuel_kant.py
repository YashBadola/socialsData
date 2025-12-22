
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_immanuel_kant_load_dataset():
    """Test that the Immanuel Kant dataset can be loaded."""
    ds = load_dataset("immanuel_kant")
    assert ds is not None
    assert len(ds) > 0
    # Check column names
    assert "text" in ds.column_names
    assert "source" in ds.column_names

def test_immanuel_kant_content():
    """Test that the content looks like Kant."""
    ds = load_dataset("immanuel_kant")

    # Check for keywords
    keywords = ["reason", "metaphysics", "a priori", "transcendental"]
    found_keywords = {k: False for k in keywords}

    # Iterate through a sample of the dataset
    for item in ds.select(range(min(100, len(ds)))):
        text = item["text"].lower()
        for k in keywords:
            if k in text:
                found_keywords[k] = True

    # Ideally we find most keywords, but at least 'reason' should be there
    assert found_keywords["reason"], "The word 'reason' should be found in Kant's text."

def test_immanuel_kant_metadata():
    """Test that metadata is correctly loaded."""
    manager = PersonalityManager()
    personality = manager.get_metadata("immanuel_kant")

    assert personality["name"] == "Immanuel Kant"
    assert "Enlightenment" in personality["system_prompt"]
    assert len(personality["sources"]) >= 2
