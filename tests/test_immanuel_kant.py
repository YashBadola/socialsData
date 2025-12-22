import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager
import pathlib

def test_immanuel_kant_dataset_loads():
    """Verify that the Immanuel Kant dataset loads correctly and contains valid data."""
    dataset = load_dataset("immanuel_kant")
    assert dataset is not None
    assert len(dataset) > 0

    # Check the first item
    item = dataset[0]
    assert "text" in item
    assert "source" in item
    assert isinstance(item["text"], str)
    assert len(item["text"]) > 0

    # Verify content relevance (checking for keywords)
    # Since dataset is chunked, we might not find specific keywords in the FIRST chunk,
    # but we can scan a few chunks or just verify it's not empty and has English words.

    found_keyword = False
    keywords = ["reason", "critique", "metaphysic", "transcendental", "priori", "duty", "imperative"]

    for i in range(min(10, len(dataset))):
        text = dataset[i]["text"].lower()
        if any(k in text for k in keywords):
            found_keyword = True
            break

    assert found_keyword, "Did not find expected Kantian keywords in the first 10 chunks."

def test_immanuel_kant_metadata():
    """Verify metadata for Immanuel Kant."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("immanuel_kant")

    assert metadata["name"] == "Immanuel Kant"
    assert metadata["id"] == "immanuel_kant"
    assert "System Prompt" in str(metadata) or "system_prompt" in str(metadata)
    assert len(metadata["sources"]) == 2
