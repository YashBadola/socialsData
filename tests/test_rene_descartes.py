import pytest
from socials_data.core.manager import PersonalityManager
from socials_data.core.loader import load_dataset
import os
from pathlib import Path

def test_rene_descartes_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "rene_descartes" in personalities

def test_rene_descartes_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("rene_descartes")
    assert metadata["name"] == "Rene Descartes"
    assert metadata["id"] == "rene_descartes"
    assert "Cogito, ergo sum" in metadata["system_prompt"]
    assert len(metadata["sources"]) >= 3

def test_load_dataset():
    # Test loading the processed dataset
    dataset = load_dataset("rene_descartes")
    assert dataset is not None
    assert len(dataset) > 0

    # Check sample content
    sample = dataset[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Check for keywords
    found_cogito = False
    found_method = False

    for item in dataset:
        text = item["text"].lower()
        if "reason" in text or "method" in text:
            found_method = True
        if "god" in text or "mind" in text:
            found_cogito = True

        if found_method and found_cogito:
            break

    assert found_method, "Did not find expected keywords in the dataset"
    assert found_cogito, "Did not find expected keywords in the dataset"

def test_data_integrity():
    dataset = load_dataset("rene_descartes")
    for item in dataset:
        assert item["text"].strip() != "", "Found empty text in dataset"
