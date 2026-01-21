from socials_data import load_dataset
import pytest

def test_soren_kierkegaard_dataset():
    # Verify we can load the data we just created
    ds = load_dataset("soren_kierkegaard")

    # Check that we have at least one entry
    assert len(ds) > 0

    # Check content of the first entry or aggregate
    all_text = " ".join([item["text"] for item in ds])

    # Verify some key phrases exist in the text
    assert "The crowd is untruth" in all_text
    assert "Anxiety is the dizziness of freedom" in all_text
    assert "Truth is subjectivity" in all_text

    # Check source field
    assert ds[0]["source"] == "excerpts.txt"
