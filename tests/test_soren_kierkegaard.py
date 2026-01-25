from socials_data import load_dataset
import pytest

def test_soren_kierkegaard_dataset():
    # Load the dataset
    dataset = load_dataset("soren_kierkegaard")

    # Check length: we added 2 text files, so there should be 2 items in default text split
    assert len(dataset) == 2

    # Check content
    all_text = " ".join([item["text"] for item in dataset])

    # Check for key phrases
    assert "Knight of Faith" in all_text
    assert "Despair is the sickness unto death" in all_text

if __name__ == "__main__":
    test_soren_kierkegaard_dataset()
