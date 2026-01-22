import pytest
from socials_data import load_dataset

def test_kierkegaard_dataset():
    """Test that the Soren Kierkegaard dataset loads and contains expected text."""
    dataset = load_dataset("soren_kierkegaard")
    assert len(dataset) > 0, "Dataset should not be empty"

    # Collect all text
    all_text = " ".join([item["text"] for item in dataset])

    # Check for content from Fear and Trembling
    assert "Teleological Suspension of the Ethical" in all_text
    assert "Knight of Faith" in all_text

    # Check for content from Either/Or
    assert "Diapsalmata" in all_text
    assert "Rotation Method" in all_text

    # Check for specific phrase
    assert "I don't feel like doing anything" in all_text
