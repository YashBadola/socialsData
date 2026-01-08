import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

def test_load_dataset_arthur_schopenhauer():
    """Test loading the Arthur Schopenhauer dataset."""
    dataset = load_dataset("arthur_schopenhauer")

    # Check if dataset is not empty
    assert len(dataset) > 0

    # Check structure of the first item
    first_item = dataset[0]
    assert "text" in first_item
    assert "source" in first_item

    # Check source content
    # Note: The source field in processed data is the filename
    sources = set(item["source"] for item in dataset)
    expected_sources = {"the_world_as_will_and_idea_vol1.txt", "essays_of_schopenhauer.txt"}

    # Use set intersection to verify at least some expected sources are present
    assert len(sources.intersection(expected_sources)) > 0

    # Basic content check
    # Check for keywords that should appear in Schopenhauer's text
    keywords = ["will", "representation", "suffering", "world", "schopenhauer"]
    found_keywords = False

    for item in dataset.select(range(min(100, len(dataset)))):
        text = item["text"].lower()
        if any(keyword in text for keyword in keywords):
            found_keywords = True
            break

    assert found_keywords, "Failed to find characteristic keywords in the dataset sample"

def test_metadata_arthur_schopenhauer():
    """Test metadata for Arthur Schopenhauer."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("arthur_schopenhauer")

    assert metadata["name"] == "Arthur Schopenhauer"
    assert "system_prompt" in metadata
    assert len(metadata["sources"]) == 2
