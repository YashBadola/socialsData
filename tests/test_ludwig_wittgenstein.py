from socials_data import load_dataset
import pytest

def test_ludwig_wittgenstein_dataset():
    """
    Test that the Ludwig Wittgenstein dataset loads correctly and contains expected content.
    """
    dataset = load_dataset("ludwig_wittgenstein")

    # We expect 2 items corresponding to the 2 raw files
    assert len(dataset) == 2

    # Collect all text to search within it
    all_text = " ".join([item["text"] for item in dataset])

    # Check for Tractatus content
    assert "The world is everything that is the case" in all_text
    assert "Whereof one cannot speak, thereof one must remain silent" in all_text

    # Check for Investigations content
    assert "language-game" in all_text
    assert "shew the fly the way out of the fly-bottle" in all_text

if __name__ == "__main__":
    test_ludwig_wittgenstein_dataset()
