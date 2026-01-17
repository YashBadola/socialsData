import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager
import os

def test_kierkegaard_exists():
    """Test that Soren Kierkegaard personality is correctly registered."""
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "soren_kierkegaard" in personalities

def test_kierkegaard_metadata():
    """Test that metadata for Soren Kierkegaard is valid."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("soren_kierkegaard")
    assert metadata["name"] == "Søren Kierkegaard"
    assert "existentialist" in metadata["description"]
    assert len(metadata["sources"]) > 0

def test_kierkegaard_data_loading():
    """Test that processed data for Soren Kierkegaard can be loaded."""
    # Assuming data has been processed in previous steps
    dataset = load_dataset("soren_kierkegaard")
    assert len(dataset) > 0
    assert "text" in dataset[0]

    # Check for content from the raw files
    text_content = [item['text'] for item in dataset]
    found_keyword = any("The Unhappiest Man" in text for text in text_content)
    assert found_keyword, "Could not find 'The Unhappiest Man' in processed data"

def test_kierkegaard_qa_loading():
    """Test that QA pairs for Soren Kierkegaard can be loaded (if supported by loader or manually checked)."""
    # Ideally the loader supports 'qa' split, but based on README it might default to 'text'.
    # We can check the file existence at least.
    qa_path = os.path.join("socials_data", "personalities", "soren_kierkegaard", "processed", "qa.jsonl")
    assert os.path.exists(qa_path)

    import json
    with open(qa_path, 'r') as f:
        qa_pairs = [json.loads(line) for line in f]

    assert len(qa_pairs) > 0
    assert "instruction" in qa_pairs[0]
    assert "response" in qa_pairs[0]
    assert "faith" in str(qa_pairs).lower()
