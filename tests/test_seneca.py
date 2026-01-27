from socials_data import load_dataset
import pytest

def test_seneca_dataset():
    """
    Test that the Seneca dataset can be loaded and contains expected content.
    """
    # Load the dataset
    ds = load_dataset("seneca")

    # Check that we have 4 items (corresponding to our 4 files)
    assert len(ds) == 4

    # Collect all text
    all_text = " ".join([item["text"] for item in ds])

    # Check for specific phrases from our raw data

    # From Letter 1
    assert "set yourself free for your own sake" in all_text
    assert "Nothing, Lucilius, is ours, except time" in all_text

    # From Letter 7
    assert "Do you ask me what you should regard as especially to be avoided? I say, crowds" in all_text

    # From Letter 18
    assert "It is the month of December, and yet the city is at this very moment in a sweat" in all_text
    assert "Start practicing poverty" in all_text

    # From On the Shortness of Life
    assert "It is not that we have a short time to live, but that we waste a lot of it" in all_text
    assert "The part of life we really live is small" in all_text

    print("Seneca dataset verified successfully!")

if __name__ == "__main__":
    test_seneca_dataset()
