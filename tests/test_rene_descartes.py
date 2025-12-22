import pytest
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset
import os

def test_personality_metadata_integrity():
    """Test that the Rene Descartes personality has valid metadata."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("rene_descartes")

    assert metadata["id"] == "rene_descartes"
    assert metadata["name"] == "Rene Descartes"
    assert "Discourse on the Method" in [s["title"] for s in metadata["sources"]]
    assert metadata["system_prompt"] is not None
    assert "Cogito, ergo sum" in metadata["system_prompt"]

def test_dataset_loading():
    """Test that the dataset can be loaded using the hf dataset loader."""
    dataset = load_dataset("rene_descartes")

    # Check if dataset is not empty
    assert len(dataset) > 0

    # Check the schema
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Verify content relevance (checking for keywords)
    # Since we have chunks, we might need to search a few to find keywords,
    # but let's just check that text is string and non-empty.
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Let's try to find a specific keyword in the first few samples to ensure it's not garbage
    # We'll check the first 20 samples for "God", "mind", "reason", "method", or "thought"
    found_keyword = False
    keywords = ["God", "mind", "reason", "method", "thought", "soul", "body", "existence"]

    # Hugging Face dataset slicing returns a dict of lists
    samples = dataset[:50]["text"]
    for text in samples:
        if any(k in text for k in keywords) or any(k.lower() in text.lower() for k in keywords):
            found_keyword = True
            break

    assert found_keyword, "Did not find expected keywords in the first 50 samples."

if __name__ == "__main__":
    test_personality_metadata_integrity()
    test_dataset_loading()
    print("All tests passed!")
