import os
import pytest
from socials_data import load_dataset

def test_soren_kierkegaard_dataset():
    """Test that the Søren Kierkegaard dataset loads correctly."""
    dataset = load_dataset("soren_kierkegaard")

    assert dataset is not None
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Check for some keywords specific to Kierkegaard or the text
    # "aesthetic", "ethical", "religious", "individual", "crowd" are good candidates,
    # but we should check what's actually in the text we downloaded.
    # The file includes "Diapsalmata", "Fear and Trembling".

    # Let's search for a keyword that should definitely be there.
    found_keyword = False
    keywords = ["Kierkegaard", "aesthetic", "ethical", "faith", "Abraham", "Isaac", "infinite"]

    # We iterate a few samples to find keywords
    for i in range(min(len(dataset), 100)):
        text = dataset[i]["text"]
        if any(k in text for k in keywords):
            found_keyword = True
            break

    assert found_keyword, "Could not find expected keywords in the first 100 samples."

if __name__ == "__main__":
    # Manually run the test function if executed as a script
    try:
        test_soren_kierkegaard_dataset()
        print("Test passed!")
    except AssertionError as e:
        print(f"Test failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
