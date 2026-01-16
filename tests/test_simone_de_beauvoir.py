from socials_data.core.loader import load_dataset
import pytest

def test_load_dataset():
    """Test loading the Simone de Beauvoir dataset."""
    dataset = load_dataset("simone_de_beauvoir")

    assert len(dataset) > 0
    assert "text" in dataset[0]

    # Check if the text comes from our expected sources
    sources = set([item["source"] for item in dataset])
    assert "existential_ambiguity.txt" in sources
    assert "on_the_other.txt" in sources
    assert "letter_to_sartre.txt" in sources

    # Simple content check
    assert any("The Second Sex" in item["text"] for item in dataset if item["source"] == "on_the_other.txt") or \
           any("The category of the Other" in item["text"] for item in dataset if item["source"] == "on_the_other.txt")
