from socials_data import load_dataset
import pytest

def test_machiavelli_dataset():
    # Load the dataset
    ds = load_dataset("niccolo_machiavelli")

    # We expect 2 items: The Prince and Discourses
    assert len(ds) == 2

    # Check for content
    all_text = " ".join([item["text"] for item in ds])

    # Specific phrases from The Prince
    assert "Nicolo Machiavelli" in all_text
    assert "The Prince" in all_text
    # Specific phrases from Discourses
    assert "Discourses on the First Decade of Titus Livius" in all_text

    # Check that sources are correct
    sources = [item["source"] for item in ds]
    assert "the_prince.txt" in sources
    assert "discourses_on_livy.txt" in sources

if __name__ == "__main__":
    test_machiavelli_dataset()
