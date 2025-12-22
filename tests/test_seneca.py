
import pytest
from socials_data import load_dataset

def test_load_seneca():
    dataset = load_dataset("seneca")
    assert len(dataset) > 0

    first_item = dataset[0]
    assert "text" in first_item
    assert isinstance(first_item["text"], str)

    # Check for some keywords that should be in Seneca's text
    keywords = ["benefit", "gratitude", "virtue", "nature", "mind"]

    # The dataset when sliced returns a dict of lists, not a list of dicts.
    # dataset[:5]["text"] gives a list of texts.
    text_sample = " ".join(dataset[:5]["text"]).lower()

    found_keywords = [kw for kw in keywords if kw in text_sample]
    assert len(found_keywords) > 0, f"None of the keywords {keywords} found in the first 5 chunks."

if __name__ == "__main__":
    test_load_seneca()
    print("Test passed!")
