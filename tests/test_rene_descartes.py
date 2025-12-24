
import os
import pytest
from socials_data.core.loader import load_dataset

def test_load_rene_descartes_dataset():
    # Load the dataset
    ds = load_dataset("rene_descartes")

    # Check if dataset is not empty
    assert len(ds) > 0

    # Check first item structure
    first_item = ds[0]
    assert "text" in first_item
    assert "source" in first_item

    # Check for specific keywords to verify content
    keywords = ["God", "mind", "reason", "soul", "exist"]

    # Iterate through a few samples to ensure keywords appear
    found_keywords = set()
    for item in ds:
        text = item["text"]
        for kw in keywords:
            if kw in text:
                found_keywords.add(kw)
        if len(found_keywords) == len(keywords):
            break

    # We expect to find at least some keywords
    assert len(found_keywords) > 0

    # Check if sources are correct
    sources = set(item["source"] for item in ds)
    assert "discourse_on_the_method.txt" in sources
    assert "meditations.txt" in sources

if __name__ == "__main__":
    # Manually run the test function if executed as a script
    try:
        test_load_rene_descartes_dataset()
        print("Test passed!")
    except AssertionError as e:
        print(f"Test failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
