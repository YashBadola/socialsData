from socials_data import load_dataset
import pytest

def test_ludwig_wittgenstein_dataset():
    """Verify that the Ludwig Wittgenstein dataset loads and contains expected data."""
    dataset = load_dataset("ludwig_wittgenstein")

    # Check that we have at least one entry
    assert len(dataset) > 0

    # Combine all text to search for key phrases
    all_text = " ".join([item["text"] for item in dataset])

    # Check for specific phrases
    assert "The world is everything that is the case" in all_text
    assert "Whereof one cannot speak, thereof one must be silent" in all_text
    assert "meaning of a word is its use" in all_text

if __name__ == "__main__":
    test_ludwig_wittgenstein_dataset()
