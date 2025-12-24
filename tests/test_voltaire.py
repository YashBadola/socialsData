
import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_voltaire_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("voltaire")
    assert metadata["name"] == "Voltaire"
    assert metadata["id"] == "voltaire"
    assert "Enlightenment" in metadata["description"]
    assert len(metadata["sources"]) >= 4

def test_load_voltaire_dataset():
    # PYTHONPATH=. is needed if running this manually, but via pytest it should be handled if conftest or similar is set up.
    # But here we are just importing.
    dataset = load_dataset("voltaire")
    assert len(dataset) > 0

    # Check first item
    first_item = dataset[0]
    assert "text" in first_item
    assert "source" in first_item
    assert len(first_item["text"]) > 10

def test_content_quality():
    dataset = load_dataset("voltaire")

    # Check for unwanted artifacts in a sample
    # Note: Dataset is large, so we sample.

    # Check for Project Gutenberg headers which should be gone
    for i in range(min(len(dataset), 50)):
        text = dataset[i]["text"]
        assert "Project Gutenberg" not in text
        assert "START OF THE PROJECT" not in text
        assert "Distributed Proofreading Team" not in text

def test_specific_works_present():
    dataset = load_dataset("voltaire")
    sources = set([item["source"] for item in dataset])

    expected_sources = ["candide.txt", "zadig.txt", "micromegas.txt", "philosophical_dictionary.txt"]
    for source in expected_sources:
        assert source in sources
