import os
import pytest
from socials_data import load_dataset

def test_load_dataset_immanuel_kant():
    """Test that the Immanuel Kant dataset can be loaded and contains valid data."""
    dataset = load_dataset("immanuel_kant")

    assert dataset is not None, "Dataset should not be None"
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check the first example
    example = dataset[0]
    assert "text" in example, "Example should contain 'text' field"
    assert isinstance(example["text"], str), "'text' field should be a string"
    assert len(example["text"]) > 0, "'text' field should not be empty"

    # Check for keywords that should appear in Kant's works
    # Using a subset of possible keywords since the text is chunked
    keywords = ["reason", "critique", "moral", "imperative", "transcendental", "priori", "duty", "metaphysic"]

    # Verify at least one keyword appears in the first few chunks
    found_keyword = False
    for i in range(min(10, len(dataset))):
        text = dataset[i]["text"].lower()
        if any(k in text for k in keywords):
            found_keyword = True
            break

    assert found_keyword, f"Should find at least one of {keywords} in the first 10 chunks"

def test_file_structure():
    """Verify that the necessary files exist."""
    base_path = "socials_data/personalities/immanuel_kant"
    assert os.path.exists(os.path.join(base_path, "metadata.json")), "metadata.json should exist"
    assert os.path.exists(os.path.join(base_path, "raw", "critique_of_pure_reason.txt")), "critique_of_pure_reason.txt should exist"
    assert os.path.exists(os.path.join(base_path, "raw", "fundamental_principles_metaphysic_morals.txt")), "fundamental_principles_metaphysic_morals.txt should exist"
    assert os.path.exists(os.path.join(base_path, "processed", "data.jsonl")), "processed/data.jsonl should exist"
