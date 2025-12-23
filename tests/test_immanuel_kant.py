import pytest
import os
import json
from socials_data.core.manager import PersonalityManager
from socials_data.core.loader import load_dataset
from pathlib import Path

def test_immanuel_kant_metadata():
    """Verify that Immanuel Kant metadata is correct and follows the schema."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("immanuel_kant")

    assert metadata["name"] == "Immanuel Kant"
    assert metadata["id"] == "immanuel_kant"
    assert "transcendental idealism" in metadata["description"]
    assert "categorical imperative" in metadata["system_prompt"]
    assert len(metadata["sources"]) == 2

    source_titles = [s["title"] for s in metadata["sources"]]
    assert "The Critique of Pure Reason" in source_titles
    assert "The Critique of Practical Reason" in source_titles

def test_immanuel_kant_processed_data():
    """Verify that the processed data loads correctly and contains expected content."""
    # Ensure the dataset can be loaded
    dataset = load_dataset("immanuel_kant")

    assert len(dataset) > 0

    # Check sample content
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Check that we have content from both books in the dataset
    sources = set(dataset["source"])
    assert "critique_of_pure_reason.txt" in sources
    assert "critique_of_practical_reason.txt" in sources

def test_immanuel_kant_content_relevance():
    """Verify that the text content is actually related to Kant."""
    dataset = load_dataset("immanuel_kant")

    # Simple keyword check in a random sample
    keywords = ["reason", "priori", "posteriori", "moral", "imperative", "transcendental", "intuition", "concept"]

    found_keywords = 0
    checked_samples = 0

    # Check first 50 samples or all if less
    for i in range(min(len(dataset), 50)):
        text = dataset[i]["text"].lower()
        if any(k in text for k in keywords):
            found_keywords += 1
        checked_samples += 1

    # At least 80% of samples should contain relevant keywords
    assert found_keywords / checked_samples > 0.8

def test_no_gutenberg_headers():
    """Verify that Gutenberg headers are stripped."""
    dataset = load_dataset("immanuel_kant")

    for i in range(min(len(dataset), 100)):
        text = dataset[i]["text"]
        assert "PROJECT GUTENBERG EBOOK" not in text
        assert "START OF THE PROJECT" not in text
