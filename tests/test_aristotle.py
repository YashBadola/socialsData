from socials_data import load_dataset
import pytest

def test_aristotle_dataset():
    # Load the Aristotle dataset
    dataset = load_dataset("aristotle")

    # Check if we have at least 3 records (we created 3 files)
    assert len(dataset) >= 3

    # Verify content presence
    all_text = " ".join([item["text"] for item in dataset])
    assert "Man is by nature a political animal" in all_text
    assert "Happiness, then, is something final and self-sufficient" in all_text
    assert "All men by nature desire to know" in all_text

if __name__ == "__main__":
    test_aristotle_dataset()
