
import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_thomas_hobbes_data():
    """Verify that Thomas Hobbes data can be loaded and contains expected content."""

    # 1. Check Metadata
    manager = PersonalityManager()
    metadata = manager.get_metadata("thomas_hobbes")
    assert metadata["name"] == "Thomas Hobbes"
    assert metadata["id"] == "thomas_hobbes"
    assert "Leviathan" in metadata["sources"][0]["title"]

    # 2. Check Dataset Loading
    # Use load_dataset from the package
    dataset = load_dataset("thomas_hobbes")
    assert len(dataset) > 0

    # 3. Check Content
    # Check for a known phrase from Leviathan
    # "solitary, poor, nasty, brutish, and short" is the most famous, let's see if it's in there.
    # Note: Text is chunked, so we iterate to find it.
    found_quote = False
    keyword = "nasty, brutish, and short"

    # Get a sample
    for i in range(min(len(dataset), 100)):
        text = dataset[i]["text"]
        if keyword in text:
            found_quote = True
            break

    # If not found in first 100, might be deeper or slightly different punctuation.
    # Let's try "Artificial Animal" which is in the intro we saw.
    if not found_quote:
        keyword_intro = "Artificial Animal"
        for i in range(len(dataset)):
             if keyword_intro in dataset[i]["text"]:
                 found_quote = True
                 break

    assert found_quote, "Could not find expected text content in the dataset."

    # 4. Check Structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] == "leviathan.txt"

if __name__ == "__main__":
    test_thomas_hobbes_data()
