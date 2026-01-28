import pytest
from socials_data.core.manager import PersonalityManager
import os
import json
from socials_data import load_dataset

def test_schopenhauer_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "arthur_schopenhauer" in personalities

def test_schopenhauer_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("arthur_schopenhauer")
    assert metadata["name"] == "Arthur Schopenhauer"
    assert metadata["id"] == "arthur_schopenhauer"
    titles = [s["title"] for s in metadata["sources"]]
    assert "The World as Will and Representation" in titles

def test_schopenhauer_data_loaded():
    dataset = load_dataset("arthur_schopenhauer")
    assert len(dataset) >= 3

    # Check for keywords
    # Flatten all text to search
    all_text = " ".join([d["text"] for d in dataset])

    assert "Will" in all_text
    assert "representation" in all_text
    assert "suffering" in all_text

    # Check source tracking
    sources = [d["source"] for d in dataset]
    assert "the_world_as_will.txt" in sources
    assert "studies_in_pessimism.md" in sources
