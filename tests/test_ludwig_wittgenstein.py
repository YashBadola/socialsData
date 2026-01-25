import pytest
from pathlib import Path
from socials_data.core.loader import load_dataset, PERSONALITIES_DIR

def test_load_wittgenstein_dataset():
    """Test that the Ludwig Wittgenstein dataset can be loaded and contains valid data."""
    dataset = load_dataset("ludwig_wittgenstein")

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check the structure of the first item
    first_item = dataset[0]
    assert "text" in first_item, "Item should contain 'text' field"
    assert "source" in first_item, "Item should contain 'source' field"

    # Check sources
    sources = set(item["source"] for item in dataset)
    expected_sources = {"tractatus.txt"}

    # We might add more files later, but for now ensure tractatus is there
    assert "tractatus.txt" in sources

    # Specific keywords we expect in Wittgenstein's text
    keywords = ["world", "logic", "fact", "silent", "limits"]
    found_keywords = False
    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]:
                found_keywords = True
                break
        if found_keywords:
            break

    assert found_keywords, "Did not find expected keywords in the dataset"

def test_qa_file_exists():
    """Test that the QA file exists (since we manually created it)."""
    qa_path = PERSONALITIES_DIR / "ludwig_wittgenstein" / "processed" / "qa.jsonl"

    assert qa_path.exists(), "QA file should exist"
    assert qa_path.stat().st_size > 0, "QA file should not be empty"

if __name__ == "__main__":
    test_load_wittgenstein_dataset()
    test_qa_file_exists()
