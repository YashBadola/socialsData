import pytest
from socials_data.core.loader import load_dataset

def test_load_kierkegaard_dataset():
    """Test that the Kierkegaard dataset can be loaded and contains valid data."""
    dataset = load_dataset("soren_kierkegaard")

    assert len(dataset) > 0, "Dataset should not be empty"

    first_item = dataset[0]
    assert "text" in first_item, "Item should contain 'text' field"
    assert "source" in first_item, "Item should contain 'source' field"

    # Check for specific keywords
    keywords = ["Faith", "paradox", "individual", "despair", "self", "Knight of Faith"]
    found = False
    for item in dataset:
        for k in keywords:
            if k in item["text"]:
                found = True
                break
        if found: break

    assert found, "Did not find expected keywords in the dataset"

if __name__ == "__main__":
    test_load_kierkegaard_dataset()
