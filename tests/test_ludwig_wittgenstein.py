from socials_data import load_dataset
import pytest

def test_ludwig_wittgenstein_loading():
    """
    Tests that the Ludwig Wittgenstein dataset loads correctly.
    """
    ds = load_dataset("ludwig_wittgenstein")

    # We populated it with 2 records (from data.jsonl)
    assert len(ds) == 2

    # Check content
    all_text = " ".join([item["text"] for item in ds])
    assert "The world is all that is the case" in all_text
    assert "meaning of a word is its use" in all_text

    # Check source
    sources = [item["source"] for item in ds]
    assert "tractatus_excerpt.txt" in sources
    assert "investigations_excerpt.txt" in sources

if __name__ == "__main__":
    test_ludwig_wittgenstein_loading()
