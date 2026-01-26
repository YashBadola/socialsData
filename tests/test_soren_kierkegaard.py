from socials_data import load_dataset
import pytest

def test_soren_kierkegaard_dataset():
    """
    Verifies that the Søren Kierkegaard dataset loads correctly and contains the expected content.
    """
    # Load the dataset
    dataset = load_dataset("soren_kierkegaard")

    # We added 3 files, so we expect at least 3 records.
    # Depending on how the processor chunks, it might be exactly 3 if each file is small enough.
    assert len(dataset) >= 3

    # Collect all text to search for key phrases
    all_text = " ".join([item["text"] for item in dataset])

    # Check for phrases from Fear and Trembling
    assert "Infinite resignation is the last stage prior to faith" in all_text
    assert "Abraham was greater than all" in all_text

    # Check for phrases from Either/Or
    assert "Marry, and you will regret it" in all_text
    assert "The unhappy person is one who has his ideal" in all_text

    # Check for phrases from The Sickness Unto Death
    assert "The self is a relation that relates itself to itself" in all_text
    assert "Despair is the sickness unto death" in all_text

if __name__ == "__main__":
    test_soren_kierkegaard_dataset()
