from socials_data.core.loader import load_dataset
import pytest

def test_load_soren_kierkegaard_dataset():
    dataset = load_dataset("soren_kierkegaard")

    # Check if dataset is loaded
    assert len(dataset) > 0

    # Check content of first entry
    first_entry = dataset[0]
    assert "text" in first_entry
    assert "source" in first_entry
    assert first_entry["source"] == "excerpts.txt"
    assert "Man is spirit" in first_entry["text"]
