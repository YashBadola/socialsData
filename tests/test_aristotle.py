from socials_data import load_dataset
import pytest

def test_aristotle_dataset():
    # Load the dataset
    ds = load_dataset("aristotle")

    # We added 3 text files, so there should be 3 items in the text split
    # Note: load_dataset currently defaults to 'text' split
    assert len(ds) == 3

    # Check for content from each file
    all_text = " ".join([item["text"] for item in ds])

    # Check for Nicomachean Ethics content
    assert "Virtue, then, is a state of character concerned with choice" in all_text

    # Check for Politics content
    # Note: the text file has "man is more of a political animal", let's check a unique substring
    # checking "political animal" should be safe
    assert "political animal" in all_text

    # Check for Metaphysics content
    assert "All men by nature desire to know" in all_text

if __name__ == "__main__":
    test_aristotle_dataset()
