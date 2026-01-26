from socials_data import load_dataset
import pytest

def test_wittgenstein_data():
    ds = load_dataset("ludwig_wittgenstein")
    assert len(ds) == 2

    all_text = " ".join([item["text"] for item in ds])
    assert "The world is all that is the case" in all_text
    assert "meaning of a word is its use" in all_text

    # Check for sources
    sources = [item["source"] for item in ds]
    assert "tractatus_excerpt.txt" in sources
    assert "investigations_excerpt.txt" in sources

if __name__ == "__main__":
    test_wittgenstein_data()
