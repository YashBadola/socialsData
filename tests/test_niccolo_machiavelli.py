import os
import pytest
from socials_data.core.loader import load_dataset
import json

@pytest.fixture
def niccolo_machiavelli_dataset():
    # Force reload or ensure it picks up the local directory
    # The load_dataset function in this repo likely loads from the local processed/ directory
    # based on the ID passed.
    return load_dataset("niccolo_machiavelli")

def test_niccolo_machiavelli_dataset_structure(niccolo_machiavelli_dataset):
    dataset = niccolo_machiavelli_dataset

    # Check if it is a Dataset object
    # In this repo, load_dataset might return a Hugging Face Dataset or similar.
    # The memory says "The load_dataset function returns a Hugging Face Dataset object"
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check columns
    expected_columns = ["text", "source"]
    for col in expected_columns:
        assert col in dataset.column_names, f"Column {col} missing"

def test_niccolo_machiavelli_content(niccolo_machiavelli_dataset):
    dataset = niccolo_machiavelli_dataset

    # Check sources
    sources = set(dataset["source"])
    expected_sources = {
        "the_prince.txt",
        "discourses_on_livy.txt",
        "history_of_florence.txt"
    }

    # We might have more or fewer depending on how splitting works, but sources should match
    # filenames.
    assert sources.issubset(expected_sources) or expected_sources.issubset(sources), f"Unexpected sources: {sources}"

    # Sample checks
    texts = dataset["text"]

    # Check for some known phrases
    prince_text = next((t for t, s in zip(texts, dataset["source"]) if s == "the_prince.txt"), None)
    assert prince_text is not None
    # "All states, all powers" is the start of Chapter I usually.
    # Or "Niccolo Machiavelli to the Magnificent Lorenzo" if dedication is included.
    # We stripped dedication header but kept body.
    assert "Lorenzo" in prince_text or "states" in prince_text.lower()

    discourses_text = next((t for t, s in zip(texts, dataset["source"]) if s == "discourses_on_livy.txt"), None)
    assert discourses_text is not None
    # Should contain "Rome" or "Republic"
    assert "Rome" in discourses_text

    history_text = next((t for t, s in zip(texts, dataset["source"]) if s == "history_of_florence.txt"), None)
    assert history_text is not None
    assert "Florence" in history_text

def test_metadata_completeness():
    metadata_path = os.path.join("socials_data", "personalities", "niccolo_machiavelli", "metadata.json")
    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    assert metadata["name"] == "Niccolò Machiavelli"
    assert metadata["id"] == "niccolo_machiavelli"
    assert "system_prompt" in metadata
    assert len(metadata["system_prompt"]) > 100
    assert len(metadata["sources"]) == 3
