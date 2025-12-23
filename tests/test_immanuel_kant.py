import pytest
from socials_data import load_dataset

def test_immanuel_kant_dataset_structure():
    """
    Test that the Immanuel Kant dataset can be loaded and has the correct structure.
    """
    try:
        # Load the dataset for immanuel_kant
        dataset = load_dataset("immanuel_kant")
    except Exception as e:
        pytest.fail(f"Failed to load immanuel_kant dataset: {e}")

    # Check if the dataset is not empty
    assert len(dataset) > 0, "The dataset should not be empty."

    # Check the features of the dataset
    assert "text" in dataset.column_names, "Dataset should contain 'text' column."
    assert "source" in dataset.column_names, "Dataset should contain 'source' column."

    # Check the content of the first few examples
    for i in range(min(5, len(dataset))):
        example = dataset[i]
        assert isinstance(example["text"], str), f"Text in example {i} should be a string."
        assert len(example["text"]) > 0, f"Text in example {i} should not be empty."
        assert isinstance(example["source"], str), f"Source in example {i} should be a string."
        # Verify that the source is one of the expected filenames
        assert example["source"] in [
            "critique_of_pure_reason.txt",
            "critique_of_practical_reason.txt",
            "fundamental_principles_of_the_metaphysic_of_morals.txt"
        ], f"Unexpected source file: {example['source']}"

def test_immanuel_kant_content_keywords():
    """
    Test that the content of the dataset contains keywords relevant to Kant.
    """
    dataset = load_dataset("immanuel_kant")

    # Define some keywords that should appear in Kant's works
    keywords = ["reason", "pure", "practical", "moral", "imperative", "transcendental", "critique"]

    found_keywords = {keyword: False for keyword in keywords}

    # Check a subset of the dataset for keywords (to avoid scanning everything if large)
    # We scan up to 100 entries or the whole dataset
    for i in range(min(100, len(dataset))):
        text = dataset[i]["text"].lower()
        for keyword in keywords:
            if keyword in text:
                found_keywords[keyword] = True

    # It's possible not ALL keywords appear in the first 100 chunks, but "reason" certainly should.
    assert found_keywords["reason"], "The keyword 'reason' was not found in the first 100 chunks."
