from socials_data import load_dataset
import pytest

def test_soren_kierkegaard_dataset():
    """Test that the Søren Kierkegaard dataset loads correctly and contains expected text."""
    # Load the dataset for Søren Kierkegaard
    dataset = load_dataset("soren_kierkegaard")

    # Check if we have data
    assert len(dataset) > 0

    # Concatenate all text to check for key phrases
    all_text = " ".join([item["text"] for item in dataset])

    # Check for phrases from our raw files
    assert "The Knight of Faith" in all_text
    assert "The Sickness Unto Death" in all_text
    assert "teleological suspension" in all_text
    assert "synthesis of the infinite and the finite" in all_text

    # Verify source field exists
    assert "source" in dataset[0]

if __name__ == "__main__":
    test_soren_kierkegaard_dataset()
