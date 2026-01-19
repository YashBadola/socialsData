from socials_data import load_dataset
import pytest

def test_rousseau_dataset():
    # Load the dataset
    ds = load_dataset("jean_jacques_rousseau")

    # Check number of records
    assert len(ds) == 2

    # Check sources
    sources = set(item['source'] for item in ds)
    assert "social_contract.txt" in sources
    assert "discourse_on_inequality.txt" in sources

    # Check content availability
    # We combine all text to search for key phrases
    all_text = " ".join([item["text"] for item in ds])

    # Phrases to check
    # Depending on the Gutenberg version, headers might be part of the file but cleaned.
    # The cleaning script removes Gutenberg headers but keeps the title page usually.

    assert "Social Contract" in all_text or "SOCIAL CONTRACT" in all_text
    assert "Inequality" in all_text or "INEQUALITY" in all_text

if __name__ == "__main__":
    test_rousseau_dataset()
