import os
import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

def test_immanuel_kant_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "immanuel_kant" in personalities

def test_immanuel_kant_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("immanuel_kant")
    assert metadata["name"] == "Immanuel Kant"
    assert len(metadata["sources"]) == 5
    assert "transcendental" in metadata["system_prompt"]

def test_immanuel_kant_dataset_load():
    # Only load the 'text' subset (which is the default or handled by load_dataset)
    # The load_dataset function in this repo returns a Hugging Face dataset.
    dataset = load_dataset("immanuel_kant")
    assert len(dataset) > 0

    # Check content of a few samples
    sample_text = dataset[0]["text"]
    assert isinstance(sample_text, str)
    assert len(sample_text) > 0

    # Search for characteristic Kantian terms in the whole dataset (or a subset)
    found_term = False
    for i in range(min(100, len(dataset))):
        text = dataset[i]["text"]
        if "reason" in text.lower() or "imperative" in text.lower() or "priori" in text.lower():
            found_term = True
            break
    assert found_term, "Could not find characteristic terms (reason, imperative, priori) in the first 100 samples"

def test_no_gutenberg_header():
    dataset = load_dataset("immanuel_kant")
    # Check first and last few entries for Gutenberg boilerplate
    for i in range(min(5, len(dataset))):
        text = dataset[i]["text"]
        assert "Project Gutenberg" not in text
        assert "START OF THIS PROJECT GUTENBERG EBOOK" not in text
