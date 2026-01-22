from socials_data import load_dataset
import pytest

def test_sartre_loading():
    ds = load_dataset("jean_paul_sartre")
    assert len(ds) > 0, "Dataset should not be empty"

    # Check if text contains key phrases
    first_text = ds[0]["text"]

    # Normalize whitespace for searching
    normalized_text = first_text.replace("\n", " ")

    assert "Existentialism Is a Humanism" in normalized_text
    assert "existence precedes essence" in normalized_text
    assert "condemned to be free" in normalized_text

if __name__ == "__main__":
    test_sartre_loading()
