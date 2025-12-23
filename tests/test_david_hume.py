import pytest
from socials_data import load_dataset
from datasets import Dataset

def test_david_hume_dataset_loading():
    """Test that the David Hume dataset loads correctly."""
    dataset = load_dataset("david_hume")
    assert isinstance(dataset, Dataset)
    assert len(dataset) > 0

    # Check first item
    first_item = dataset[0]
    assert "text" in first_item
    assert "source" in first_item

    # Check that sources are correct
    sources = set(dataset["source"])
    assert "a_treatise_of_human_nature.txt" in sources or "an_enquiry_concerning_human_understanding.txt" in sources

def test_david_hume_content():
    """Test that the content seems relevant to Hume."""
    dataset = load_dataset("david_hume")

    # Search for key terms
    text_content = " ".join(dataset[:10]["text"]).lower()
    keywords = ["idea", "impression", "reason", "passion", "nature"]

    found = any(k in text_content for k in keywords)
    assert found, "Did not find expected keywords in the first few samples."
