import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

@pytest.fixture
def manager():
    return PersonalityManager()

def test_jean_jacques_rousseau_metadata(manager):
    meta = manager.get_metadata("jean_jacques_rousseau")
    assert meta["name"] == "Jean-Jacques Rousseau"
    assert "public domain" in meta["license"].lower()
    assert len(meta["sources"]) >= 3
    assert any("Social Contract" in s["title"] for s in meta["sources"])

def test_jean_jacques_rousseau_dataset_loading():
    dataset = load_dataset("jean_jacques_rousseau")

    # Check if dataset is not empty
    assert len(dataset) > 0

    # Check column names
    assert "text" in dataset.column_names
    assert "source" in dataset.column_names

    # Check content of a sample
    sample = dataset[0]
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Verify sources
    sources = set(dataset["source"])
    assert "social_contract_and_discourses.txt" in sources
    assert "emile.txt" in sources
    assert "confessions.txt" in sources

def test_jean_jacques_rousseau_content_cleaning():
    dataset = load_dataset("jean_jacques_rousseau")

    # Sample verification to ensure Gutenberg headers are gone
    # We check a random sample of texts
    for item in dataset.select(range(min(100, len(dataset)))):
        text = item["text"]
        # Basic check for Gutenberg boilerplate which usually has "Project Gutenberg"
        # Note: Some mentions might exist in the text if Rousseau mentions it (impossible),
        # or if the cleaner missed something.
        # But usually we want to avoid the license block.
        assert "Project Gutenberg License" not in text
        assert "START OF THE PROJECT GUTENBERG" not in text

def test_jean_jacques_rousseau_keywords():
    dataset = load_dataset("jean_jacques_rousseau")

    # Check for presence of key terms
    all_text = " ".join(dataset[:100]["text"]).lower()

    # Keywords likely to appear
    keywords = ["nature", "man", "law", "will", "social", "inequality"]
    found_keywords = [k for k in keywords if k in all_text]

    # We expect most keywords to be present in a large sample
    assert len(found_keywords) >= 3
