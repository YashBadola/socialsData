import pytest
from socials_data import load_dataset

def test_load_wittgenstein_dataset():
    """Test that the Wittgenstein dataset can be loaded and contains valid data."""
    dataset = load_dataset("ludwig_wittgenstein")
    assert len(dataset) > 0, "Dataset should not be empty"

    first_item = dataset[0]
    assert "text" in first_item
    assert isinstance(first_item["text"], str)

    # Check for key phrases
    keywords = ["world", "case", "logic", "proposition", "fact"]
    found = False
    for item in dataset:
        if any(k in item["text"] for k in keywords):
            found = True
            break
    assert found, "Did not find expected keywords"

if __name__ == "__main__":
    test_load_wittgenstein_dataset()
