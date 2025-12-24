import pytest
import os
import json
from socials_data import load_dataset

def test_load_rene_descartes_dataset():
    """Test that the Rene Descartes dataset loads correctly."""
    try:
        dataset = load_dataset("rene_descartes")
    except ValueError as e:
        pytest.fail(f"Failed to load dataset: {e}")

    assert len(dataset) > 0, "Dataset is empty"

    # Check for expected content
    sample_text = dataset[0]["text"]
    assert isinstance(sample_text, str), "Text should be a string"
    assert len(sample_text) > 0, "Text should not be empty"

    # Check for key terms
    keywords = ["Descartes", "God", "reason", "mind", "soul", "body"]
    found_keywords = []

    # Check first 100 samples for keywords
    for i in range(min(len(dataset), 100)):
        text = dataset[i]["text"]
        for keyword in keywords:
            if keyword in text and keyword not in found_keywords:
                found_keywords.append(keyword)

    assert len(found_keywords) > 0, f"No keywords found in dataset. Looked for {keywords}"

def test_metadata_consistency():
    """Test that metadata.json is consistent with processed data."""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    metadata_path = os.path.join(base_path, "socials_data", "personalities", "rene_descartes", "metadata.json")

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    assert metadata["id"] == "rene_descartes"
    assert "René Descartes" in metadata["name"]
    assert len(metadata["sources"]) == 3

if __name__ == "__main__":
    pytest.main([__file__])
