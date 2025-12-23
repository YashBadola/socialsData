import os
import pytest
from socials_data import load_dataset

@pytest.fixture
def john_locke_dataset():
    return load_dataset("john_locke")

def test_load_dataset(john_locke_dataset):
    assert john_locke_dataset is not None
    # We expect some data
    assert len(john_locke_dataset) > 0

def test_content_structure(john_locke_dataset):
    sample = john_locke_dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert isinstance(sample["source"], str)

def test_content_keywords(john_locke_dataset):
    # Check for keywords related to Locke in the dataset
    keywords = ["understanding", "ideas", "mind", "government", "political", "power"]

    found_keywords = {k: False for k in keywords}

    # Check a subset of samples to avoid long runtimes
    for i in range(min(100, len(john_locke_dataset))):
        text = john_locke_dataset[i]["text"].lower()
        for k in keywords:
            if k in text:
                found_keywords[k] = True

    # We expect at least some of these keywords to be present across the dataset
    assert any(found_keywords.values()), f"None of the keywords {keywords} found in the first 100 samples."

def test_sources(john_locke_dataset):
    sources = set(john_locke_dataset["source"])
    expected_sources = {
        "essay_concerning_human_understanding_vol1.txt",
        "essay_concerning_human_understanding_vol2.txt",
        "second_treatise_of_government.txt"
    }
    assert expected_sources.issubset(sources)
