from socials_data import load_dataset
import pytest

def test_diogenes_dataset():
    """
    Test that the Diogenes of Sinope dataset loads correctly and contains expected content.
    """
    ds = load_dataset("diogenes_of_sinope")

    # We expect at least one record
    assert len(ds) >= 1

    # Check for content from the raw file
    all_text = " ".join([item["text"] for item in ds])

    # Check for key anecdotes
    assert "looking for a human" in all_text
    assert "Stand a little out of my sun" in all_text
    assert "Plato's man" in all_text
    assert "citizen of the world" in all_text

if __name__ == "__main__":
    test_diogenes_dataset()
