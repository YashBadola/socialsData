import os
import pytest
from socials_data.core.loader import load_dataset

def test_load_sartre_dataset():
    """Test that the Jean-Paul Sartre dataset can be loaded and contains valid data."""
    dataset = load_dataset("jean_paul_sartre")

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
    expected_sources = {"existentialism_is_a_humanism.txt", "being_and_nothingness.txt", "nausea.txt"}

    # Check that sources match expected sources
    assert sources == expected_sources, f"Expected sources {expected_sources}, but got {sources}"

    # Specific keywords we expect in Sartre's text
    keywords = ["existentialism", "freedom", "responsibility", "nothingness", "bad faith"]
    found_keywords = False
    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]:
                found_keywords = True
                break
        if found_keywords:
            break

    assert found_keywords, "Did not find expected keywords in the dataset"

    # Check for Q&A data
    # Since load_dataset only loads the main data, we need to manually check for qa.jsonl
    qa_path = os.path.join(os.path.dirname(__file__), "../socials_data/personalities/jean_paul_sartre/processed/qa.jsonl")
    assert os.path.exists(qa_path), "qa.jsonl should exist"

    import json
    with open(qa_path, 'r') as f:
        qa_data = [json.loads(line) for line in f]

    assert len(qa_data) > 0, "qa.jsonl should not be empty"
    first_qa = qa_data[0]
    assert "instruction" in first_qa, "QA item should have instruction"
    assert "response" in first_qa, "QA item should have response"
    assert "source" in first_qa, "QA item should have source"

if __name__ == "__main__":
    test_load_sartre_dataset()
