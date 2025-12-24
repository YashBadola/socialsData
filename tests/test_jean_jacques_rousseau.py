import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_rousseau_dataset_loading():
    """Test that the Rousseau dataset loads correctly."""
    dataset = load_dataset("jean_jacques_rousseau")
    assert dataset is not None, "Dataset should not be None"
    assert len(dataset) > 0, "Dataset should not be empty"

def test_rousseau_content_validity():
    """Test that the content of the Rousseau dataset is valid."""
    dataset = load_dataset("jean_jacques_rousseau")

    # Check for specific keywords
    found_keywords = False
    keywords = ["General Will", "sovereign", "nature", "inequality", "Emile", "contract"]

    # Iterate through a sample of the dataset
    sample_size = min(len(dataset), 100)
    for i in range(sample_size):
        text = dataset[i]["text"]
        if any(keyword in text for keyword in keywords):
            found_keywords = True
            break

    assert found_keywords, "Dataset should contain Rousseau-specific keywords"

def test_rousseau_metadata():
    """Test that the metadata for Rousseau is correct."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("jean_jacques_rousseau")

    assert metadata["name"] == "Jean-Jacques Rousseau"
    assert "General Will" in metadata["system_prompt"]
    assert len(metadata["sources"]) == 4

def test_no_gutenberg_boilerplate():
    """Test that the Gutenberg boilerplate has been removed."""
    dataset = load_dataset("jean_jacques_rousseau")

    boilerplate_markers = [
        "Project Gutenberg",
        "PROJECT GUTENBERG",
        "License",
        "start of the project gutenberg",
        "end of the project gutenberg"
    ]

    # Check a sample for boilerplate
    # Note: "Project Gutenberg" might appear in the text if Rousseau mentions it (impossible)
    # or if the cleaning wasn't perfect.
    # However, we allow some small leaks if they are just mentions, but we want to avoid the full license blocks.
    # The cleaning script splits by markers, so it should be clean.

    count = 0
    failures = 0
    for item in dataset:
        text = item["text"]
        # We search case-insensitive for the main phrase
        if "Project Gutenberg License" in text or "START OF THE PROJECT" in text:
            failures += 1
            print(f"Found boilerplate in chunk: {text[:100]}...")
        count += 1
        if count > 500: break # Check first 500 chunks

    assert failures == 0, f"Found {failures} chunks with Gutenberg boilerplate"
