from socials_data import load_dataset
import pytest

def test_soren_kierkegaard_dataset():
    # Load the dataset
    dataset = load_dataset("soren_kierkegaard")

    # Check length (we have 3 files)
    assert len(dataset) == 3

    # Check content
    all_text = " ".join([item["text"] for item in dataset])

    # Key phrases
    assert "The Sickness Unto Death is Despair" in all_text
    assert "What is a poet?" in all_text
    assert "Faith is precisely this paradox" in all_text
    assert "teleological suspension of the ethical" in all_text

if __name__ == "__main__":
    test_soren_kierkegaard_dataset()
