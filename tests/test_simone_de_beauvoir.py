import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_simone_de_beauvoir_exists():
    pm = PersonalityManager()
    personalities = pm.list_personalities()
    assert "simone_de_beauvoir" in personalities

def test_simone_de_beauvoir_load_dataset():
    # Attempt to load the dataset
    dataset = load_dataset("simone_de_beauvoir")

    # Check that it's not empty
    assert len(dataset) > 0

    # Verify the structure of the first item
    first_item = dataset[0]
    assert "text" in first_item
    assert "source" in first_item

    # Check content of one of the items
    texts = [item['text'] for item in dataset]
    found_intro = any("For a long time I have hesitated to write a book on woman" in text for text in texts)
    assert found_intro, "Intro text not found in dataset"
