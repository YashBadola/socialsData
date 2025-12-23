
import os
import pytest
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset
import json

def test_immanuel_kant_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("immanuel_kant")

    assert metadata["name"] == "Immanuel Kant"
    assert metadata["id"] == "immanuel_kant"
    assert "system_prompt" in metadata
    assert len(metadata["sources"]) == 3

    source_titles = [s["title"] for s in metadata["sources"]]
    assert "The Critique of Pure Reason" in source_titles
    assert "The Critique of Practical Reason" in source_titles
    assert "The Critique of Judgement" in source_titles

def test_immanuel_kant_dataset_load():
    # Load the dataset
    dataset = load_dataset("immanuel_kant")

    assert len(dataset) > 0

    # Check a sample
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Verify sources are present in the dataset
    sources = set(dataset["source"])
    assert "critique_of_pure_reason.txt" in sources
    assert "critique_of_practical_reason.txt" in sources
    assert "critique_of_judgement.txt" in sources

def test_content_keywords():
    dataset = load_dataset("immanuel_kant")

    # Check for some Kantian keywords in the text
    keywords = ["reason", "priori", "transcendental", "judgment", "practical"]

    found_keywords = set()
    for item in dataset:
        text = item["text"].lower()
        for kw in keywords:
            if kw in text:
                found_keywords.add(kw)
        if len(found_keywords) == len(keywords):
            break

    assert len(found_keywords) > 0, "No keywords found in dataset"

if __name__ == "__main__":
    # Manually run if executed as script
    try:
        test_immanuel_kant_metadata()
        print("Metadata test passed")
        test_immanuel_kant_dataset_load()
        print("Dataset load test passed")
        test_content_keywords()
        print("Content keywords test passed")
    except Exception as e:
        print(f"Tests failed: {e}")
        exit(1)
