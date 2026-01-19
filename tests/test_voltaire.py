from socials_data import load_dataset
import pytest

def test_voltaire_dataset():
    """
    Test that the Voltaire dataset loads correctly and contains data.
    """
    # Load the dataset
    dataset = load_dataset("voltaire")

    # Check if dataset is not empty
    assert len(dataset) > 0

    # Check if 'text' column exists
    assert "text" in dataset[0]

    # Check if specific content exists in the dataset
    texts = [row["text"] for row in dataset]
    candide_found = any("CANDIDE" in text for text in texts)
    assert candide_found

    # Check sources
    sources = [row["source"] for row in dataset]
    assert "candide_chap1.txt" in sources
