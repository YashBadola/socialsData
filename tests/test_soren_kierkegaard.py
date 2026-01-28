from socials_data import load_dataset
import pytest

def test_soren_kierkegaard_dataset():
    # Load the dataset for Soren Kierkegaard
    dataset = load_dataset("soren_kierkegaard")

    # Check if we have 3 items (since we added 3 files)
    assert len(dataset) == 3

    # Concatenate all text to search for keywords
    all_text = " ".join([item["text"] for item in dataset])

    # Check for specific phrases from our raw data
    assert "The Sickness Unto Death is Despair" in all_text
    assert "Knight of Faith" in all_text
    assert "What is a poet?" in all_text
    assert "tyrant Phalaris" in all_text

    print("Soren Kierkegaard dataset test passed!")

if __name__ == "__main__":
    test_soren_kierkegaard_dataset()
