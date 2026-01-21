import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_soren_kierkegaard_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("soren_kierkegaard")

    assert metadata["name"] == "Søren Kierkegaard"
    assert metadata["id"] == "soren_kierkegaard"
    assert len(metadata["sources"]) == 3
    assert metadata["sources"][0]["title"] == "Either/Or"

def test_soren_kierkegaard_dataset_structure():
    """Verify that the dataset loads and has the correct structure."""
    dataset = load_dataset("soren_kierkegaard")

    # Check if dataset is not empty
    assert len(dataset) > 0

    # Check column names
    assert "text" in dataset.column_names
    assert "source" in dataset.column_names

    # Verify content presence (simple check)
    all_text = " ".join(dataset["text"])
    assert "Anxiety is the dizziness of freedom." in all_text
    assert "The Sickness Unto Death" in all_text

    # Verify sources
    sources = set(dataset["source"])
    assert "quotes.txt" in sources
    assert "excerpts_philosophical.txt" in sources
    assert "sickness_unto_death_excerpt.txt" in sources
