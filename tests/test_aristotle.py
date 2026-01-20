from socials_data import load_dataset
import pytest

def test_aristotle_dataset():
    ds = load_dataset("aristotle")
    assert len(ds) >= 1

    # Check for some characteristic text
    # The first line of the actual text
    expected_text = "Every art, and every science reduced to a teachable form"

    found = False
    for item in ds:
        if expected_text in item["text"]:
            found = True
            break

    assert found
