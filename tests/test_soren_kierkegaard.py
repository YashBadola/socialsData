from socials_data import load_dataset
import pytest

def test_soren_kierkegaard_dataset():
    # Load the dataset
    ds = load_dataset("soren_kierkegaard")

    # Check if we have 3 items
    assert len(ds) == 3

    # Combine all text
    all_text = " ".join([item["text"] for item in ds])

    # Check for specific phrases from our raw data
    assert "The concept of despair" in all_text
    assert "Knight of Faith" in all_text
    assert "Diapsalmata" in all_text
    assert "What is a poet?" in all_text
    assert "The Rotation Method" in all_text

if __name__ == "__main__":
    test_soren_kierkegaard_dataset()
