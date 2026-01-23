from socials_data import load_dataset
import pytest

def test_soren_kierkegaard_dataset():
    # Load the dataset
    ds = load_dataset("soren_kierkegaard")

    # Assert that we have at least 3 entries (since we have 3 raw files)
    assert len(ds) >= 3

    # Concatenate all text to search for phrases
    all_text = " ".join([item["text"] for item in ds])

    # Check for specific phrases from our simulated data
    assert "Man is spirit. But what is spirit?" in all_text
    assert "Faith is precisely this paradox" in all_text
    assert "What is a poet? An unhappy man" in all_text
    assert "My soul is like a dead sea" in all_text

if __name__ == "__main__":
    test_soren_kierkegaard_dataset()
