from socials_data import load_dataset
import pytest

def test_heraclitus_dataset():
    # Verify we can load the data
    dataset = load_dataset("heraclitus")

    # Check if we have entries. We created 6 raw files, so we expect 6 entries in the dataset.
    assert len(dataset) == 6

    all_text = " ".join([item["text"] for item in dataset])

    # Check for iconic phrases
    assert "Into the same river you could not step twice" in all_text
    assert "War is the father and king of all" in all_text
    assert "The way upward and downward are one and the same" in all_text
    assert "Homer deserved to be driven out of the lists and flogged" in all_text
    assert "Time is a child playing at draughts" in all_text

if __name__ == "__main__":
    test_heraclitus_dataset()
