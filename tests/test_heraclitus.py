import pytest
from socials_data import load_dataset

def test_heraclitus_dataset():
    """Test that the Heraclitus dataset loads and contains the correct data."""
    dataset = load_dataset("heraclitus")

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check the first item structure
    item = dataset[0]
    assert "text" in item
    assert "source" in item
    assert item["source"] == "fragments.txt"

    # Check for key phrases
    text = item["text"]
    assert "Logos" in text
    assert "river" in text
    assert "Fire" in text
    assert "War is the father of all" in text
    assert "Nature loves to hide" in text

if __name__ == "__main__":
    test_heraclitus_dataset()
