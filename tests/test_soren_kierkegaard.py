import pytest
import os
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_soren_kierkegaard_dataset_loading():
    """Test that the Soren Kierkegaard dataset loads correctly."""
    dataset = load_dataset("soren_kierkegaard")

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check schema
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Check content relevance
    text_content = ""
    for item in dataset:
        text_content += item["text"]

    # Keywords expected in Kierkegaard's work
    keywords = ["anxiety", "faith", "Abraham", "aesthetic", "ethical", "poet", "paradox"]
    found_keywords = [kw for kw in keywords if kw.lower() in text_content.lower()]
    assert len(found_keywords) > 0, f"Expected to find some Kierkegaardian keywords, but found: {found_keywords}"

    # Negative assertion: check that Gutenberg license is cleaned out
    assert "Project Gutenberg License" not in text_content
    assert "gutenberg.org" not in text_content

def test_soren_kierkegaard_metadata():
    """Test that metadata exists and is correct."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("soren_kierkegaard")

    assert metadata["name"] == "Soren Kierkegaard"
    assert metadata["id"] == "soren_kierkegaard"
    assert metadata["license"] == "Public Domain"
    assert len(metadata["sources"]) > 0
    assert "system_prompt" in metadata
    assert "existentialist" in metadata["description"].lower()

if __name__ == "__main__":
    pytest.main([__file__])
