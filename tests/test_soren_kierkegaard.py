from socials_data.core.loader import load_dataset
import pytest

def test_kierkegaard_dataset_loading():
    """Test that the Søren Kierkegaard dataset loads correctly."""
    dataset = load_dataset("soren_kierkegaard")

    assert len(dataset) > 0
    assert "text" in dataset[0]

    # Check for specific content we know is in there
    found_text = False
    for item in dataset:
        if "Faith is precisely this paradox" in item["text"]:
            found_text = True
            break

    assert found_text, "Expected text from Fear and Trembling not found in dataset"
