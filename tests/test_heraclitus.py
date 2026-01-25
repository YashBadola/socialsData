from socials_data import load_dataset
import pytest

def test_heraclitus_dataset():
    """
    Tests that the Heraclitus dataset loads correctly and contains expected fragments.
    """
    dataset = load_dataset("heraclitus")

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"

    # Combine all text to search for keywords
    all_text = " ".join([item["text"] for item in dataset])

    # Check for specific fragments from our raw files
    assert "ever-living Fire" in all_text
    assert "step twice into the same rivers" in all_text
    assert "self-multiplying Logos" in all_text
    assert "glutted like beasts" in all_text

    # Check sources
    sources = [item["source"] for item in dataset]
    assert "fire_and_cosmos.txt" in sources
    assert "flux.txt" in sources
    assert "logos.txt" in sources
    assert "human_folly.txt" in sources
    print("Test passed successfully!")

if __name__ == "__main__":
    test_heraclitus_dataset()
