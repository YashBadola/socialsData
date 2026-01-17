from socials_data import load_dataset
import pytest
import re

def test_jean_jacques_rousseau_dataset():
    # Load the dataset for Jean-Jacques Rousseau
    ds = load_dataset("jean_jacques_rousseau")

    # Check if the dataset is not empty
    assert len(ds) > 0, "Dataset should not be empty"

    # Check if specific content exists in the dataset
    all_text = " ".join([item["text"] for item in ds])

    # Normalize whitespace to single spaces
    all_text_normalized = re.sub(r'\s+', ' ', all_text)

    # Assertions based on "The Social Contract"
    assert "Man is born free; and everywhere he is in chains" in all_text_normalized
    assert "THE SOCIAL CONTRACT" in all_text_normalized
    assert "Each of us puts his person and all his power in common under the supreme direction of the general will" in all_text_normalized

if __name__ == "__main__":
    test_jean_jacques_rousseau_dataset()
