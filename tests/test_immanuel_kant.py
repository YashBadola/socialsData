import os
import pytest
from socials_data import load_dataset

def test_load_dataset_immanuel_kant():
    """Verify that the Immanuel Kant dataset loads and contains valid data."""
    dataset = load_dataset("immanuel_kant")

    # Check that it's a Hugging Face Dataset
    assert hasattr(dataset, "column_names"), "Object should be a HF Dataset"
    assert "text" in dataset.column_names
    assert "source" in dataset.column_names

    # Verify content
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check sample content
    sample = dataset[0]
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0
    assert sample["source"] == "critique_of_pure_reason.txt"

    # Verify relevance keywords (check a few samples if needed)
    text_content = " ".join([d["text"] for d in dataset.select(range(min(10, len(dataset))))])
    keywords = ["reason", "pure", "critique", "philosophy", "metaphysics"]

    found_keywords = [kw for kw in keywords if kw.lower() in text_content.lower()]
    assert len(found_keywords) > 0, f"Expected to find some of {keywords} in the text"

if __name__ == "__main__":
    pytest.main([__file__])
