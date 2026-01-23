from socials_data import load_dataset
import pytest

def test_load_heraclitus_dataset():
    """Test that the Heraclitus dataset can be loaded and contains valid data."""
    dataset = load_dataset("heraclitus")

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check the structure of the first item
    first_item = dataset[0]
    assert "text" in first_item, "Item should contain 'text' field"
    assert "source" in first_item, "Item should contain 'source' field"

    # Check content of the text
    text = first_item["text"]
    assert isinstance(text, str), "Text should be a string"
    assert len(text) > 0, "Text should not be empty"

    # Check sources
    sources = set(item["source"] for item in dataset)
    expected_sources = {"fragments.txt"}
    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"

    # Specific keywords we expect in Heraclitus's text
    keywords = ["Logos", "river", "fire", "war", "change"]
    found_keywords = False

    # Since there is likely one big item, we check if keywords are in it.
    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]:
                found_keywords = True
                # We want to find at least one, but ideally all are there.
                # Let's check for "Logos" specifically to be sure.
                if keyword == "Logos":
                     assert keyword in item["text"]

    assert found_keywords, "Did not find expected keywords in the dataset"

    # Check for a specific fragment part
    assert "No man ever steps in the same river twice" in text or "step into the same rivers" in text

if __name__ == "__main__":
    test_load_heraclitus_dataset()
