from socials_data import load_dataset
import pytest

def test_ludwig_wittgenstein_loading():
    """
    Test that the Ludwig Wittgenstein dataset loads correctly and contains expected content.
    """
    ds = load_dataset("ludwig_wittgenstein")
    assert len(ds) == 2

    all_text = " ".join([item["text"] for item in ds])

    # Check for content from Tractatus
    assert "The world is all that is the case" in all_text
    assert "Whereof one cannot speak" in all_text

    # Check for content from Investigations
    assert "Excalibur" in all_text
    assert "language-game" in all_text

if __name__ == "__main__":
    test_ludwig_wittgenstein_loading()
