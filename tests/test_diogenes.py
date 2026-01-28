from socials_data import load_dataset
import pytest

def test_diogenes_data():
    ds = load_dataset("diogenes_of_sinope")
    # We have 2 raw files (anecdotes.txt, sayings.txt), so we expect 2 records
    assert len(ds) == 2

    all_text = " ".join([item["text"] for item in ds])

    # Check for specific famous quotes
    assert "Stand a little out of my sunshine" in all_text or "stand a little out of my sunshine" in all_text
    assert "I am looking for a human" in all_text
    assert "banish hunger by rubbing the belly" in all_text

    # Check that sources are correct
    sources = [item["source"] for item in ds]
    assert "anecdotes.txt" in sources
    assert "sayings.txt" in sources

if __name__ == "__main__":
    test_diogenes_data()
