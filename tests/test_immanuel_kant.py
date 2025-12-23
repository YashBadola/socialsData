import pytest
from socials_data.core.loader import load_dataset

def test_load_immanuel_kant_dataset():
    """Test that the Immanuel Kant dataset loads correctly and contains valid data."""
    dataset = load_dataset("immanuel_kant")

    assert dataset is not None, "Dataset should not be None"
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check the first sample
    sample = dataset[0]
    assert "text" in sample, "Sample should contain 'text' field"
    assert "source" in sample, "Sample should contain 'source' field"
    assert isinstance(sample["text"], str), "Text should be a string"
    assert len(sample["text"]) > 0, "Text should not be empty"

def test_kant_content_keywords():
    """Test that the dataset contains characteristic Kantian terminology."""
    dataset = load_dataset("immanuel_kant")

    # Check for keywords in a subset of the data
    keywords = ["reason", "moral", "law", "imperative", "transcendental", "priori", "duty"]
    found_keywords = {k: False for k in keywords}

    # Scan first 100 samples or all if less
    scan_limit = min(len(dataset), 100)
    for i in range(scan_limit):
        text = dataset[i]["text"].lower()
        for keyword in keywords:
            if keyword in text:
                found_keywords[keyword] = True

    # We expect at least some of these to be found in 100 random chunks of Kant
    found_count = sum(found_keywords.values())
    assert found_count > 0, f"No Kantian keywords found in first {scan_limit} samples"
