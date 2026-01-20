from socials_data import load_dataset
import pytest

def test_jean_jacques_rousseau_dataset():
    dataset = load_dataset("jean_jacques_rousseau")
    assert len(dataset) == 2

    all_text = " ".join([item["text"] for item in dataset])

    # Check Social Contract content
    assert "Man is born free" in all_text

    # Check Confessions content
    # I'll check for "enterprise which has no precedent" which is in the intro of Book I usually.
    # Let's verify what "BOOK I." is followed by in my file.
    # But "I have resolved on an enterprise" is classic.
    # If regex search was case sensitive, I should be careful.

    assert "social contract" in all_text.lower()
    assert "confessions" in all_text.lower()

if __name__ == "__main__":
    test_jean_jacques_rousseau_dataset()
