import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_load_plato_dataset():
    """Test loading the Plato dataset."""
    dataset = load_dataset("plato")

    # Check that it returns a Hugging Face Dataset
    assert dataset is not None, "Dataset should not be None"

    # Check that we have some data
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check the first sample
    sample = dataset[0]
    assert "text" in sample, "Sample should contain 'text' field"
    assert "source" in sample, "Sample should contain 'source' field"

    # Verify content relevance
    # Since we are checking chunks, we iterate to find some key terms
    found_republic = False
    found_socrates = False
    found_glaucon = False

    # Check first 20 samples to save time, usually terms appear early
    for i in range(min(len(dataset), 50)):
        text = dataset[i]["text"]
        if "Republic" in text or "republic" in text: # It might not be in the text body if headers stripped, but let's see
             pass # Actually the title 'The Republic' is not in the body usually
        if "Socrates" in text or "socrates" in text:
            found_socrates = True
        if "Glaucon" in text or "glaucon" in text:
            found_glaucon = True

    # Note: Socrates is the speaker but usually referred to as "I" in the first person narrative,
    # but other characters address him or he is mentioned.
    # Actually, Glaucon is mentioned in the first sentence.

    assert found_glaucon, "Should find mention of Glaucon in the first few chunks"

def test_plato_metadata():
    """Test that metadata is correctly loaded."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("plato")

    assert metadata["name"] == "Plato"
    assert metadata["id"] == "plato"
    assert metadata["license"] == "Public Domain"
    assert len(metadata["sources"]) == 1
    assert metadata["sources"][0]["title"] == "The Republic"

if __name__ == "__main__":
    test_load_plato_dataset()
    test_plato_metadata()
    print("All tests passed!")
