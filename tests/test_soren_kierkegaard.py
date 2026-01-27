from socials_data import load_dataset
import pytest

def test_soren_kierkegaard_dataset():
    # Load the dataset
    ds = load_dataset("soren_kierkegaard")

    # Check if we have 3 items (from 3 raw files)
    assert len(ds) == 3

    # Collect all text
    all_text = " ".join([item["text"] for item in ds])

    # Check for key phrases from our simulated excerpts
    assert "What is a poet?" in all_text
    assert "The ethical is the universal" in all_text
    assert "Despair is the sickness unto death" in all_text
    assert "knight of faith" in all_text
    assert "tyrant Phalaris" in all_text

    # Check sources
    sources = [item["source"] for item in ds]
    assert "either_or.txt" in sources
    assert "fear_and_trembling.txt" in sources
    assert "sickness_unto_death.txt" in sources

if __name__ == "__main__":
    test_soren_kierkegaard_dataset()
