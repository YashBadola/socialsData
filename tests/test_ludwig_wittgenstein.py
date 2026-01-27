from socials_data import load_dataset
import pytest

def test_ludwig_wittgenstein_dataset():
    """
    Verifies that the Ludwig Wittgenstein dataset can be loaded
    and contains the expected content.
    """
    dataset = load_dataset("ludwig_wittgenstein")

    # We expect 3 entries (one per file)
    assert len(dataset) == 3

    # Check for presence of key phrases from each source
    all_text = " ".join([item["text"] for item in dataset])

    # Tractatus
    assert "The world is everything that is the case." in all_text
    assert "Whereof one cannot speak, thereof one must be silent." in all_text

    # Investigations
    assert "language-game" in all_text
    assert "beetle in the box" in all_text or "beetle" in all_text

    # Blue Book
    assert "What is the meaning of a word?" in all_text
    assert "meaning of a word is its use" in all_text

if __name__ == "__main__":
    test_ludwig_wittgenstein_dataset()
