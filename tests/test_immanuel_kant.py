import json
import pytest
from pathlib import Path
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_immanuel_kant_metadata():
    """Test that Immanuel Kant metadata is correct and loadable."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("immanuel_kant")

    assert metadata["name"] == "Immanuel Kant"
    assert metadata["id"] == "immanuel_kant"
    assert "structure of human experience" in metadata["description"]
    assert len(metadata["sources"]) == 3

    source_titles = [s["title"] for s in metadata["sources"]]
    assert "The Critique of Pure Reason" in source_titles
    assert "The Critique of Practical Reason" in source_titles
    assert "Fundamental Principles of the Metaphysic of Morals" in source_titles

def test_immanuel_kant_dataset_structure():
    """Test that the Immanuel Kant dataset loads and has the correct structure."""
    try:
        dataset = load_dataset("immanuel_kant")
    except Exception as e:
        pytest.fail(f"Failed to load dataset: {e}")

    assert len(dataset) > 0
    sample = dataset[0]

    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert isinstance(sample["source"], str)

def test_immanuel_kant_content_relevance():
    """Test that the dataset content appears to be from Kant."""
    dataset = load_dataset("immanuel_kant")

    # Check a few samples for key terms
    keywords = ["reason", "a priori", "moral", "practical", "pure", "transcendental", "imperative", "law"]

    found_keywords = set()
    for i in range(min(50, len(dataset))):
        text = dataset[i]["text"].lower()
        for keyword in keywords:
            if keyword in text:
                found_keywords.add(keyword)

    # We expect to find at least some of these keywords in the first 50 chunks
    assert len(found_keywords) > 0, "No relevant keywords found in the sample text"

def test_immanuel_kant_source_attribution():
    """Test that sources are correctly attributed."""
    dataset = load_dataset("immanuel_kant")

    sources = set()
    for item in dataset:
        sources.add(item["source"])

    expected_sources = {
        "critique_of_pure_reason.txt",
        "critique_of_practical_reason.txt",
        "metaphysic_of_morals.txt"
    }

    # We should have at least some overlap with expected sources
    assert sources.intersection(expected_sources)
