from socials_data import load_dataset
import pytest

def test_soren_kierkegaard_dataset():
    # Load the dataset
    dataset = load_dataset("soren_kierkegaard")

    # Check if we have 3 items (since we added 3 files)
    assert len(dataset) == 3

    # Check content
    all_text = " ".join([item["text"] for item in dataset])

    # Check for specific phrases from our raw files
    assert "The Sickness Unto Death" in all_text
    assert "Knight of Faith" in all_text
    assert "What is a poet?" in all_text
    assert "Teleological Suspension of the Ethical" in all_text

    # Check metadata fields are accessible (though load_dataset returns HF dataset,
    # the metadata is in the repo, but here we just check the data content)

if __name__ == "__main__":
    test_soren_kierkegaard_dataset()
