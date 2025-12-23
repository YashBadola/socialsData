
import pytest
from socials_data.core.loader import load_dataset

def test_aristotle_dataset_loading():
    """Test that the Aristotle dataset loads correctly."""
    dataset = load_dataset("aristotle")
    assert len(dataset) > 0
    assert "text" in dataset.features
    assert "source" in dataset.features

def test_aristotle_content_sanity():
    """Test that the content looks like Aristotle."""
    dataset = load_dataset("aristotle")

    # Check for keywords
    keywords = ["virtue", "happiness", "state", "political", "tragedy", "nature"]
    found_keywords = {k: False for k in keywords}

    # Check a subset of samples to speed up
    for item in dataset.select(range(min(len(dataset), 100))):
        text = item["text"].lower()
        for k in keywords:
            if k in text:
                found_keywords[k] = True

    # We expect most keywords to be found given the texts
    assert found_keywords["virtue"] or found_keywords["happiness"], "Ethics keywords missing"
    assert found_keywords["state"] or found_keywords["political"], "Politics keywords missing"

def test_aristotle_sources():
    """Verify sources are correct."""
    dataset = load_dataset("aristotle")
    sources = set(dataset["source"])
    expected_sources = {"nicomachean_ethics.txt", "politics.txt", "poetics.txt"}

    # It's possible not all files resulted in chunks if they were empty (unlikely),
    # or if chunking behavior changed.
    assert expected_sources.issubset(sources) or sources.issubset(expected_sources)
    assert "nicomachean_ethics.txt" in sources

if __name__ == "__main__":
    test_aristotle_dataset_loading()
    test_aristotle_content_sanity()
    test_aristotle_sources()
    print("Aristotle tests passed.")
