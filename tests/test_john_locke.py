import pytest
import os
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

def test_john_locke_dataset():
    # Load dataset
    dataset = load_dataset("john_locke")

    # Check structure
    assert len(dataset) > 0
    assert "text" in dataset[0]

    # Check content relevance
    content = [item["text"] for item in dataset]
    text = " ".join(content)

    # Keywords for Locke
    assert "ideas" in text.lower()
    assert "government" in text.lower()
    assert "understanding" in text.lower()

    # Check source tracking
    sources = set([item["source"] for item in dataset])
    assert "second_treatise_of_government.txt" in sources
    assert "essay_human_understanding_1.txt" in sources
    assert "essay_human_understanding_2.txt" in sources

    # Negative checks (no Gutenburg boilerplate)
    assert "Project Gutenberg" not in text
    assert "START OF THE PROJECT" not in text

def test_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("john_locke")

    assert metadata["name"] == "John Locke"
    assert "Father of Liberalism" in metadata["description"]
    assert len(metadata["sources"]) == 3
