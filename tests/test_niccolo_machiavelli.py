import os
import pytest
from socials_data.core.manager import PersonalityManager
from socials_data.core.loader import load_dataset

def test_machiavelli_personality_exists():
    pm = PersonalityManager()
    personalities = pm.list_personalities()
    assert "niccolo_machiavelli" in personalities

def test_machiavelli_metadata():
    pm = PersonalityManager()
    metadata = pm.get_metadata("niccolo_machiavelli")
    assert metadata["name"] == "Niccolò Machiavelli"
    assert "Prince" in metadata["description"]
    assert "virtù" in metadata["system_prompt"]
    assert len(metadata["sources"]) == 3

    titles = [s["title"] for s in metadata["sources"]]
    assert "The Prince" in titles
    assert "Discourses on the First Decade of Titus Livius" in titles
    assert "History of Florence" in titles

def test_machiavelli_dataset_structure():
    # Test loading the dataset
    dataset = load_dataset("niccolo_machiavelli")
    assert len(dataset) > 0

    # Check sample
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert isinstance(sample["source"], str)

def test_machiavelli_content_keywords():
    dataset = load_dataset("niccolo_machiavelli")

    # Check for keywords across a subset of samples to ensure we have the right content
    # dataset[:20] is a dict of lists like {'text': ['...', ...], 'source': [...]}, not a list of dicts.
    subset = dataset[:20]
    text_corpus = " ".join(subset["text"])

    keywords = ["Prince", "virtue", "fortune", "state", "Rome", "Florence"]
    found = {k: False for k in keywords}

    for k in keywords:
        # Case insensitive check
        if k.lower() in text_corpus.lower():
            found[k] = True

    # We expect most to be found
    assert found["Florence"] or found["Rome"] or found["state"]

def test_no_gutenberg_boilerplate():
    dataset = load_dataset("niccolo_machiavelli")

    # Iterate through the first 100 items (or fewer if dataset is small)
    num_to_check = min(len(dataset), 100)

    # Efficient access
    texts = dataset[:num_to_check]["text"]
    sources = dataset[:num_to_check]["source"]

    for i in range(num_to_check):
        text = texts[i]
        source = sources[i]
        assert "Project Gutenberg" not in text, f"Found boilerplate in source {source}"

if __name__ == "__main__":
    pytest.main([__file__])
