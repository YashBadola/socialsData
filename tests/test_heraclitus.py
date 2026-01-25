from socials_data import load_dataset
import pytest

def test_heraclitus_dataset():
    ds = load_dataset("heraclitus")
    # We created 4 raw files, so we expect 4 records in the dataset
    assert len(ds) == 4

    all_text = " ".join([item["text"] for item in ds])
    assert "Logos" in all_text
    assert "rivers" in all_text
    assert "Fire" in all_text
    assert "Ephesians" in all_text

if __name__ == "__main__":
    test_heraclitus_dataset()
