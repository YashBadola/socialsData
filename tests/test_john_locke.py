import pytest
import os
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

def test_john_locke_dataset_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "john_locke" in personalities

def test_john_locke_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("john_locke")

    assert metadata["name"] == "John Locke"
    assert "Empiricism" in metadata["system_prompt"] or "tabula rasa" in metadata["system_prompt"]
    assert len(metadata["sources"]) == 3
    assert metadata["sources"][0]["title"] == "Second Treatise of Government"

def test_john_locke_processed_data_load():
    dataset = load_dataset("john_locke")

    # Check that we have data
    assert len(dataset) > 0

    # Check schema
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Check content (smoke test)
    # We expect some key Locke terms
    all_text = " ".join([d["text"] for d in dataset])
    assert "government" in all_text.lower()
    assert "idea" in all_text.lower()

    # Check negative assertions (Gutenberg artifacts)
    assert "Project Gutenberg" not in all_text
    assert "START OF THE PROJECT" not in all_text

def test_john_locke_sources():
    dataset = load_dataset("john_locke")
    sources = set([d["source"] for d in dataset])

    assert "second_treatise_of_government.txt" in sources
    assert "essay_human_understanding_1.txt" in sources
    assert "essay_human_understanding_2.txt" in sources
