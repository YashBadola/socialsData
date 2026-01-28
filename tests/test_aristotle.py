from socials_data import load_dataset
import pytest

def test_aristotle_dataset():
    # Load the dataset
    ds = load_dataset("aristotle")

    # Check if we have at least 6 records (since we added 6 files)
    assert len(ds) >= 6

    # Concatenate all text to check for presence of key phrases
    all_text = " ".join([item["text"] for item in ds])

    # Check for specific phrases from our raw files
    assert "Every art and every inquiry" in all_text # Ethics
    assert "man is more of a political animal" in all_text # Politics
    assert "All men by nature desire to know" in all_text # Metaphysics
    assert "Tragedy, then, is an imitation of an action" in all_text # Poetics
    assert "Nature is a principle of motion and change" in all_text # Physics
    assert "Rhetoric is the counterpart of Dialectic" in all_text # Rhetoric

if __name__ == "__main__":
    test_aristotle_dataset()
