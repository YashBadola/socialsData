import os
import pytest
from socials_data import load_dataset

def test_load_dataset_jean_jacques_rousseau():
    dataset = load_dataset("jean_jacques_rousseau")
    assert len(dataset) > 0

    # Check if the dataset has the expected columns
    assert "text" in dataset.column_names
    assert "source" in dataset.column_names

    # Check content of a sample
    sample = dataset[0]
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Check for keywords that should appear in Rousseau's works
    keywords = ["inequality", "nature", "man", "society", "contract", "education", "confessions"]

    found_keywords = False
    for item in dataset:
        text = item["text"].lower()
        if any(keyword in text for keyword in keywords):
            found_keywords = True
            break

    assert found_keywords, "Did not find expected keywords in the dataset"

def test_sources_integrity():
    dataset = load_dataset("jean_jacques_rousseau")
    sources = set(dataset["source"])

    expected_sources = {
        "discourse_on_inequality.txt",
        "emile.txt",
        "the_confessions.txt",
        "the_social_contract_and_discourses.txt"
    }

    # Check that all expected sources are present
    assert expected_sources.issubset(sources)
