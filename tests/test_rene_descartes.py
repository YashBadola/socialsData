import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

@pytest.fixture
def personality_id():
    return "rene_descartes"

def test_dataset_loading(personality_id):
    """Test that the dataset loads correctly using load_dataset."""
    dataset = load_dataset(personality_id)
    assert dataset is not None
    assert len(dataset) > 0

    # Check column names
    assert "text" in dataset.column_names
    assert "source" in dataset.column_names

def test_content_relevance(personality_id):
    """Test that the content contains expected keywords."""
    dataset = load_dataset(personality_id)

    # Check for "cogito" or "think" or "method" or "God"
    keywords = ["think", "method", "reason", "God", "mind", "body"]
    found_keywords = {k: False for k in keywords}

    # Sample a few entries
    for i in range(min(20, len(dataset))):
        text = dataset[i]["text"].lower()
        for k in keywords:
            if k in text:
                found_keywords[k] = True

    # We expect at least some of these to be found across 20 chunks
    assert any(found_keywords.values()), f"None of the keywords {keywords} found in the first 20 chunks."

def test_metadata_completeness(personality_id):
    """Test that metadata fields are present."""
    manager = PersonalityManager()
    metadata = manager.get_metadata(personality_id)

    assert metadata["name"] == "René Descartes"
    assert "system_prompt" in metadata
    assert len(metadata["sources"]) == 3

def test_raw_files_exist(personality_id):
    """Test that raw files are in place."""
    base_dir = f"socials_data/personalities/{personality_id}/raw"
    expected_files = [
        "discourse_on_method.txt",
        "meditations.txt",
        "principles_of_philosophy.txt"
    ]
    for f in expected_files:
        assert os.path.exists(os.path.join(base_dir, f))
