import pytest
from socials_data.core.loader import load_dataset

def test_load_confucius_text():
    """Test that the Confucius dataset text can be loaded."""
    dataset = load_dataset("confucius")
    assert len(dataset) > 0

    first_item = dataset[0]
    assert "text" in first_item
    assert "source" in first_item
    assert "analects.txt" in first_item["source"]

def test_load_confucius_qa():
    """Test that the Confucius dataset QA can be loaded."""
    dataset = load_dataset("confucius", data_type="qa")
    assert len(dataset) > 0

    first_item = dataset[0]
    assert "instruction" in first_item
    assert "response" in first_item
    assert "source" in first_item

    assert len(first_item["response"]) > 0

if __name__ == "__main__":
    test_load_confucius_text()
    test_load_confucius_qa()
