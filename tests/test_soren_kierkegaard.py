import pytest
from socials_data.core.loader import load_dataset
import os

def test_load_dataset_soren_kierkegaard():
    """
    Tests loading the Søren Kierkegaard dataset.
    """
    # Ensure the processed data exists
    processed_file = "socials_data/personalities/soren_kierkegaard/processed/data.jsonl"
    if not os.path.exists(processed_file):
        pytest.fail(f"Processed file {processed_file} not found.")

    dataset = load_dataset("soren_kierkegaard")

    assert dataset is not None
    assert len(dataset) > 0

    # Check if the first entry has text
    assert "text" in dataset[0]

    # Check content of one of the quotes (e.g., about anxiety)
    texts = [item["text"] for item in dataset]
    found_quote = any("Anxiety is the dizziness of freedom" in text for text in texts)
    assert found_quote, "Expected quote about anxiety not found in dataset"
