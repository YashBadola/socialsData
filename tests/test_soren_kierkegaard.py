import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_soren_kierkegaard_exists():
    pm = PersonalityManager()
    personalities = pm.list_personalities()
    assert "soren_kierkegaard" in personalities

def test_soren_kierkegaard_load_dataset():
    dataset = load_dataset("soren_kierkegaard")
    assert len(dataset) > 0
    assert "text" in dataset[0]
    # Check for some characteristic text
    text_content = [item['text'] for item in dataset]
    found = False
    for text in text_content:
        if "Despair is the Sickness Unto Death" in text:
            found = True
            break
    assert found
