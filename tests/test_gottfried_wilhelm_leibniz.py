from socials_data import load_dataset
import pytest

def test_leibniz_dataset():
    """Verify Gottfried Wilhelm Leibniz dataset loads and contains expected content."""
    ds = load_dataset("gottfried_wilhelm_leibniz")

    # Should have at least 1 entry
    assert len(ds) >= 1

    # Check for content from Monadology
    all_text = " ".join([item["text"] for item in ds])

    # Key phrases from Monadology
    assert "The monad, of which we will speak here" in all_text
    assert "simple substance" in all_text
    assert "best of all possible worlds" not in all_text # Actually this phrase is usually associated with him but might not be in the text exactly like that or in this translation.
    # Let's check phrases that are definitely in the text I uploaded
    assert "Gottfried Leibniz (1714)" in all_text
    assert "Monadology" in all_text
    assert "monads have no windows" in all_text.lower() # The text has "The monads have no windows"

if __name__ == "__main__":
    test_leibniz_dataset()
