
import pytest
from socials_data import load_dataset

def test_load_plato_dataset():
    """Test loading the Plato dataset."""
    dataset = load_dataset("plato")
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check the first item
    first_item = dataset[0]
    assert "text" in first_item, "Item should contain 'text'"
    assert isinstance(first_item["text"], str), "'text' should be a string"
    assert len(first_item["text"]) > 0, "'text' should not be empty"

    # Check for specific content (random sampling)
    found_socrates = False
    for item in dataset:
        if "Socrates" in item["text"]:
            found_socrates = True
            break
    assert found_socrates, "Dataset should contain mentions of Socrates"
