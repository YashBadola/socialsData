import pytest
from socials_data import load_dataset

def test_load_machiavelli_dataset():
    """
    Test that the Machiavelli dataset loads correctly and contains the expected fields.
    """
    dataset = load_dataset("niccolo_machiavelli")
    assert len(dataset) > 0, "Dataset should not be empty"

    entry = dataset[0]
    assert "text" in entry
    assert "chapter_number" in entry
    assert "title" in entry
    assert "topics" in entry

    # Check specifically for Chapter I
    assert entry["chapter_number"] == "I"
    assert "HOW MANY KINDS" in entry["title"]
