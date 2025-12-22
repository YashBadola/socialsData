
import pytest
import os
from socials_data.core.loader import load_dataset

def test_immanuel_kant_load():
    """Test that the Immanuel Kant dataset loads correctly."""
    dataset = load_dataset("immanuel_kant")

    assert len(dataset) > 0

    # Check first item structure
    item = dataset[0]
    assert "text" in item
    assert "source" in item

    # Check that source is one of the expected files
    assert item["source"] in ["critique_of_pure_reason.txt", "critique_of_practical_reason.txt"]

    # Check for some keywords that should appear in Kant's text
    # Note: We need to search the whole dataset or a sample, as the first chunk might not have them.
    # But let's check if we can find 'reason' or 'imperative' or 'priori' in the text
    found_keyword = False
    keywords = ["reason", "pure", "practical", "priori", "imperative", "law", "duty"]

    for i in range(min(len(dataset), 20)):
        text = dataset[i]["text"].lower()
        if any(k in text for k in keywords):
            found_keyword = True
            break

    assert found_keyword, "Did not find expected keywords in the first 20 chunks"

if __name__ == "__main__":
    test_immanuel_kant_load()
