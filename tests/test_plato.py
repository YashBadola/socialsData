import pytest
from socials_data import load_dataset

def test_plato_dataset():
    """Verify that the Plato dataset loads correctly."""
    dataset = load_dataset("plato")
    assert dataset is not None, "Dataset should not be None"
    assert len(dataset) > 0, "Dataset should have records"

    # Check the first record
    sample = dataset[0]
    assert "text" in sample, "Record should contain 'text' field"
    assert "source" in sample, "Record should contain 'source' field"

    # Verify content
    text = sample["text"]
    assert isinstance(text, str), "Text should be a string"
    assert "Socrates" in text or "Republic" in text, "Text should contain expected keywords"
    assert "Project Gutenberg" not in text, "Text should be cleaned of Gutenberg headers"

if __name__ == "__main__":
    test_plato_dataset()
    print("Plato dataset verification passed!")
