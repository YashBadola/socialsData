from socials_data import load_dataset
import pytest

def test_leibniz_dataset():
    # Verify we can load the data
    ds = load_dataset("gottfried_wilhelm_leibniz")

    # We expect at least one entry
    assert len(ds) > 0

    # Check content
    all_text = " ".join([item["text"] for item in ds])

    # Normalize whitespace to single spaces for easier matching
    normalized_text = " ".join(all_text.split())

    # Check for key phrases from the Monadology
    assert "The monad, of which we will speak here, is nothing else than a simple substance" in normalized_text
    assert "The monads have no windows" in normalized_text
    assert "preestablished harmony" in normalized_text
    assert "city of God" in normalized_text

if __name__ == "__main__":
    test_leibniz_dataset()
