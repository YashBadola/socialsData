import os
import pytest
from socials_data import load_dataset

def test_load_machiavelli_dataset():
    # Load the dataset
    dataset = load_dataset("niccolo_machiavelli")

    # Check if dataset is not empty
    assert len(dataset) > 0

    # Check a sample entry
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Check sources
    sources = set(dataset["source"])
    assert "the_prince.txt" in sources or "the_prince" in sources
    assert "discourses.txt" in sources or "discourses" in sources

    # Check content relevance
    text_content = " ".join(dataset[:10]["text"])
    assert "Prince" in text_content or "Republic" in text_content or "state" in text_content or "war" in text_content

if __name__ == "__main__":
    pytest.main([__file__])
