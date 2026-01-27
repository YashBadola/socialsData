import pytest
from socials_data.core.loader import load_dataset
from pathlib import Path
import json

def test_load_laozi_dataset():
    """Test that the Laozi dataset can be loaded and contains valid data."""
    dataset = load_dataset("laozi")

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
    expected_sources = {"tao_te_ching.txt", "hua_hu_ching.txt"}

    # We expect at least one of these, but since we processed both, we should see both or check subset
    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"

    # Specific keywords we expect in Laozi's text
    keywords = ["Tao", "Way", "water", "Yin", "Yang", "soft", "sage"]
    found_keywords = False
    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]:
                found_keywords = True
                break
        if found_keywords:
            break

    assert found_keywords, "Did not find expected keywords in the dataset"

def test_laozi_qa_exists():
    """Test that the QA file exists and is valid JSONL."""
    # Assuming standard path structure relative to repo root
    qa_path = Path("socials_data/personalities/laozi/processed/qa.jsonl")
    assert qa_path.exists(), "QA file should exist"

    with open(qa_path, "r") as f:
        lines = f.readlines()
        assert len(lines) > 0, "QA file should not be empty"
        for line in lines:
            try:
                data = json.loads(line)
                assert "instruction" in data
                assert "response" in data
            except json.JSONDecodeError:
                pytest.fail("QA file contains invalid JSON")

if __name__ == "__main__":
    test_load_laozi_dataset()
    test_laozi_qa_exists()
