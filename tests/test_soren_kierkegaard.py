from socials_data import load_dataset
import pytest

def test_kierkegaard_dataset():
    # Load the dataset
    ds = load_dataset("soren_kierkegaard")

    # We expect 3 items corresponding to the 3 raw files
    assert len(ds) == 3

    # Combine all text to search for key phrases
    all_text = " ".join([item["text"] for item in ds])

    # Check for phrases from each excerpt
    assert "knight of faith" in all_text
    assert "Summa summarum" in all_text
    assert "sickness unto death" in all_text

    # Check source field
    sources = [item["source"] for item in ds]
    assert "fear_and_trembling_excerpt.txt" in sources
    assert "either_or_excerpt.txt" in sources
    assert "sickness_unto_death_excerpt.txt" in sources

if __name__ == "__main__":
    test_kierkegaard_dataset()
