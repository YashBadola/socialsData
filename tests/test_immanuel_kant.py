import os
import pytest
from socials_data import load_dataset

def test_load_dataset_immanuel_kant():
    """Verify that the Immanuel Kant dataset can be loaded and contains valid data."""
    try:
        ds = load_dataset("immanuel_kant")
    except ValueError as e:
        pytest.fail(f"Failed to load dataset: {e}")

    assert len(ds) > 0, "Dataset should not be empty"

    # Check first sample
    sample = ds[0]
    assert "text" in sample, "Sample must contain 'text' field"
    assert isinstance(sample["text"], str), "'text' field must be a string"
    assert len(sample["text"]) > 0, "'text' field must not be empty"

    # Check keywords to ensure we have the right content
    keywords = ["reason", "philosophy", "metaphysics", "transcendental", "priori", "posteriori"]
    found = False
    text_sample = sample["text"].lower()
    for kw in keywords:
        if kw in text_sample:
            found = True
            break

    assert found, f"Text should contain at least one relevant keyword from {keywords}"

if __name__ == "__main__":
    test_load_dataset_immanuel_kant()
