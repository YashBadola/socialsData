import pytest
from socials_data.core.loader import load_dataset

def test_load_bertrand_russell_text():
    dataset = load_dataset("bertrand_russell")
    assert len(dataset) > 0
    # Check for some content
    text = dataset[0]['text']
    assert isinstance(text, str)
    assert len(text) > 0
    assert dataset[0]['source'] in ["the_problems_of_philosophy.txt", "the_analysis_of_mind.txt"]
