from socials_data import load_dataset
import pytest

def test_rene_descartes():
    ds = load_dataset("rene_descartes")
    assert len(ds) > 0

    # Check for the opening sentence
    all_text = " ".join([item["text"] for item in ds])
    assert "Good sense is, of all things among men, the most equally distributed" in all_text

if __name__ == "__main__":
    test_rene_descartes()
