import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_aristotle_personality_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "aristotle" in personalities

def test_aristotle_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("aristotle")
    assert metadata["name"] == "Aristotle"
    assert metadata["id"] == "aristotle"
    assert len(metadata["sources"]) == 3
    assert metadata["sources"][0]["title"] == "The Nicomachean Ethics"

def test_aristotle_dataset_loading():
    dataset = load_dataset("aristotle")
    assert len(dataset) > 0

    # Check for content from each book
    found_ethics = False
    found_politics = False
    found_poetics = False

    for item in dataset:
        if item["source"] == "nicomachean_ethics.txt":
            found_ethics = True
        elif item["source"] == "politics.txt":
            found_politics = True
        elif item["source"] == "poetics.txt":
            found_poetics = True

        if found_ethics and found_politics and found_poetics:
            break

    assert found_ethics, "Nicomachean Ethics content not found"
    assert found_politics, "Politics content not found"
    assert found_poetics, "Poetics content not found"

def test_aristotle_content_sanity():
    dataset = load_dataset("aristotle")
    sample = dataset[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Check that we don't have Gutenberg headers
    for item in dataset.select(range(min(100, len(dataset)))):
        text = item["text"]
        assert "START OF THE PROJECT GUTENBERG EBOOK" not in text
        assert "END OF THE PROJECT GUTENBERG EBOOK" not in text

if __name__ == "__main__":
    pytest.main([__file__])
