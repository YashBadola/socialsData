from socials_data import load_dataset
import pytest

def test_ludwig_wittgenstein_dataset():
    """Test that the Ludwig Wittgenstein dataset can be loaded and contains expected content."""
    dataset = load_dataset("ludwig_wittgenstein")

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check content
    text_blob = " ".join([item["text"] for item in dataset])

    # Check for specific propositions
    assert "The world is everything that is the case" in text_blob
    assert "Whereof one cannot speak, thereof one must be silent" in text_blob
    assert "The limits of my language mean the limits of my world" in text_blob
    assert "atomic fact" in text_blob

if __name__ == "__main__":
    test_ludwig_wittgenstein_dataset()
