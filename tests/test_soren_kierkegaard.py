from socials_data import load_dataset
import pytest

def test_soren_kierkegaard_dataset():
    # Load the dataset
    ds = load_dataset("soren_kierkegaard")

    # Check that we have 2 records (one for each file)
    assert len(ds) == 2

    # Combine text to check for content
    all_text = " ".join([item["text"] for item in ds])

    # Check for specific phrases from Diapsalmata
    assert "What is a poet?" in all_text
    assert "I rather be a swineherd on Amager" in all_text

    # Check for specific phrases from Fear and Trembling
    assert "Venerable patriarch Abraham!" in all_text
    assert "struggled with God" in all_text

if __name__ == "__main__":
    test_soren_kierkegaard_dataset()
