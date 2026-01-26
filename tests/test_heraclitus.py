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
    expected_source = "fragments.txt"
    assert expected_source in sources, f"Expected source {expected_source} not found"

    # Specific keywords we expect in Heraclitus's text
    keywords = ["river", "Logos", "fire", "war", "change", "flux"]
    # Since all text might be in one block, checking the first item is sufficient if it's the only one.
    # But generally iterating is safer.

    found_keywords = []
    for keyword in keywords:
        for item in dataset:
            if keyword.lower() in item["text"].lower():
                found_keywords.append(keyword)
                break

    # We expect to find at least some of them
    assert len(found_keywords) >= 3, f"Expected at least 3 keywords, found {len(found_keywords)}: {found_keywords}"

if __name__ == "__main__":
    test_load_heraclitus_dataset()
