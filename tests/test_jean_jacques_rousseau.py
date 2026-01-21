import pytest
from socials_data import load_dataset
import os

def test_jean_jacques_rousseau_data():
    """Test that the Jean-Jacques Rousseau dataset loads correctly."""
    dataset = load_dataset("jean_jacques_rousseau")

    # Check if dataset is not empty
    assert len(dataset) > 0

    # Check if text field exists
    assert 'text' in dataset[0]

    # Check if content seems relevant (simple check)
    text = dataset[0]['text']
    assert "Jean-Jacques Rousseau" in text or "Social Contract" in text

    # Verify metadata exists
    metadata_path = os.path.join("socials_data", "personalities", "jean_jacques_rousseau", "metadata.json")
    assert os.path.exists(metadata_path)

if __name__ == "__main__":
    test_jean_jacques_rousseau_data()
