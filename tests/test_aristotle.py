
import pytest
from socials_data.core.manager import PersonalityManager
from socials_data.core.loader import load_dataset
from datasets import Dataset

def test_aristotle_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "aristotle" in personalities

def test_aristotle_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("aristotle")
    assert metadata["name"] == "Aristotle"
    assert metadata["id"] == "aristotle"
    assert "Lyceum" in metadata["system_prompt"]
    assert len(metadata["sources"]) == 3
    source_titles = [s["title"] for s in metadata["sources"]]
    assert "The Nicomachean Ethics" in source_titles
    assert "Politics" in source_titles
    assert "Poetics" in source_titles

def test_aristotle_raw_files_exist():
    manager = PersonalityManager()
    base_dir = manager.base_dir / "aristotle" / "raw"
    assert (base_dir / "nicomachean_ethics.txt").exists()
    assert (base_dir / "politics.txt").exists()
    assert (base_dir / "poetics.txt").exists()

def test_aristotle_dataset_loading():
    dataset = load_dataset("aristotle")
    assert isinstance(dataset, Dataset)
    assert len(dataset) > 0

    # Check first few samples for content
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert isinstance(sample["source"], str)

    # Check for relevant keywords in a sample (randomly checks up to 100 samples)
    relevant_keywords = ["virtue", "state", "poetry", "man", "nature", "good"]
    found_keyword = False
    for i in range(min(len(dataset), 100)):
        text = dataset[i]["text"].lower()
        if any(keyword in text for keyword in relevant_keywords):
            found_keyword = True
            break
    assert found_keyword, "No relevant keywords found in the first 100 samples."
