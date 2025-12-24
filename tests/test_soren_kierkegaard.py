import os
import pytest
from socials_data import load_dataset

def test_soren_kierkegaard_dataset():
    # Load the dataset
    dataset = load_dataset("soren_kierkegaard")

    # Check that it returns a Hugging Face Dataset
    assert str(type(dataset)) == "<class 'datasets.arrow_dataset.Dataset'>"

    # Check that we have some data
    assert len(dataset) > 0

    # Check the first example
    example = dataset[0]
    assert "text" in example
    assert "source" in example
    assert isinstance(example["text"], str)
    assert isinstance(example["source"], str)

    # Check for relevant content in the dataset (sampling a few entries)
    # Keywords related to Kierkegaard
    keywords = ["faith", "God", "individual", "Christian", "existence", "truth"]

    found_keywords = {k: False for k in keywords}

    # Check a subset of the data for efficiency
    for i in range(min(len(dataset), 100)):
        text = dataset[i]["text"]
        for k in keywords:
            if k in text:
                found_keywords[k] = True

    # We should find at least some of these keywords
    assert any(found_keywords.values()), "Did not find any expected keywords in the first 100 samples"

    # Verify metadata source matches (not strictly part of load_dataset but good to check integrity)
    # The source filename should be 'selections.txt' as that's what we named it
    sources = set(dataset["source"])
    assert "selections.txt" in sources
