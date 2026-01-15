from socials_data import load_dataset
import pytest

def test_soren_kierkegaard():
    # Verify we can load the data for Søren Kierkegaard
    ds = load_dataset("soren_kierkegaard")

    # We added 4 files, so there should be 4 items
    assert len(ds) == 4

    all_text = " ".join([item["text"] for item in ds])

    # Check for specific phrases from the files we added
    assert "The Story of Abraham" in all_text
    assert "The Sickness Unto Death" in all_text
    assert "Either/Or" in all_text
    assert "The truth is a trap" in all_text
    assert "Anxiety is the dizziness of freedom" in all_text

    print("Søren Kierkegaard test passed!")

if __name__ == "__main__":
    test_soren_kierkegaard()
