from socials_data import load_dataset
import pytest

def test_heraclitus_data():
    dataset = load_dataset("heraclitus")
    assert len(dataset) == 4

    all_text = " ".join([item["text"] for item in dataset])

    assert "You cannot step twice into the same rivers" in all_text
    assert "ever-living Fire" in all_text
    assert "Though this Word is true evermore" in all_text
    assert "The Ephesians would do well to hang themselves" in all_text

if __name__ == "__main__":
    test_heraclitus_data()
