import os
import pytest
from socials_data import load_dataset

def test_john_locke_dataset_loads():
    """Test that the John Locke dataset loads correctly and contains valid data."""
    dataset = load_dataset("john_locke")

    # Check that it's a Hugging Face Dataset
    assert str(type(dataset).__name__) == 'Dataset'

    # Check that it is not empty
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Check content relevance
    # We expect terms related to Locke's philosophy
    relevant_terms = ["government", "law", "nature", "property", "mind", "ideas", "understanding", "sensation", "reflection"]

    found_relevant = False
    for i in range(min(100, len(dataset))):
        text = dataset[i]["text"].lower()
        if any(term in text for term in relevant_terms):
            found_relevant = True
            break

    assert found_relevant, "No relevant philosophical terms found in the first 100 samples."

    # Check source filenames
    sources = set(dataset["source"])
    assert "second_treatise_of_government.txt" in sources
    assert "essay_human_understanding_vol1.txt" in sources or "essay_human_understanding_vol2.txt" in sources

if __name__ == "__main__":
    test_john_locke_dataset_loads()
    print("Test passed!")
