import pytest
from socials_data.core.loader import load_dataset

def test_load_wittgenstein_dataset():
    """Test that the Wittgenstein dataset can be loaded and contains valid data."""
    dataset = load_dataset("ludwig_wittgenstein")

    assert len(dataset) > 0, "Dataset should not be empty"

    first_item = dataset[0]
    assert "text" in first_item
    assert "source" in first_item

    sources = set(item["source"] for item in dataset)
    expected_sources = {"tractatus.txt", "investigations.txt"}
    assert sources.issubset(expected_sources)

    keywords = ["world", "facts", "language-game", "beetle", "silent"]
    found_keywords = False
    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]:
                found_keywords = True
                break
        if found_keywords:
            break

    assert found_keywords, "Did not find expected keywords in the dataset"

if __name__ == "__main__":
    test_load_wittgenstein_dataset()
