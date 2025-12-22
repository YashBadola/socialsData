import pytest
from socials_data import load_dataset

def test_load_dataset_immanuel_kant():
    """Test loading the Immanuel Kant dataset."""
    dataset = load_dataset("immanuel_kant")
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check the first sample
    sample = dataset[0]
    assert "text" in sample, "Sample should contain 'text'"
    assert isinstance(sample["text"], str), "Text should be a string"
    assert len(sample["text"]) > 0, "Text should not be empty"

    # Check that text content looks like Kant (look for specific keywords)
    # Since we are loading random chunks, we scan the whole dataset for keywords
    found_keyword = False
    keywords = ["reason", "critique", "pure", "practical", "law", "transcendental", "noumena", "phenomena", "imperative"]

    for item in dataset:
        text_lower = item["text"].lower()
        if any(keyword in text_lower for keyword in keywords):
            found_keyword = True
            break

    assert found_keyword, "Dataset should contain Kantian keywords"
