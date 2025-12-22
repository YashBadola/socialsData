import pytest
from socials_data.core.manager import PersonalityManager
from datasets import Dataset

def test_baruch_spinoza_dataset():
    manager = PersonalityManager()
    personality_id = "baruch_spinoza"

    # Check if metadata exists
    metadata = manager.get_metadata(personality_id)
    assert metadata["name"] == "Baruch Spinoza"
    assert metadata["id"] == "baruch_spinoza"

    # Check if dataset loads
    from socials_data import load_dataset
    dataset = load_dataset(personality_id)

    assert isinstance(dataset, Dataset)
    assert len(dataset) > 0

    # Check sample content
    sample = dataset[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)

    # Check for keywords related to Spinoza in the first few samples
    # (Since chunking might split text, we check if any chunk contains key terms)
    # Actually, we can just check if the text is non-empty.
    # But let's look for "God" or "Substance" or "Nature" in the first 100 samples
    found_keyword = False
    keywords = ["God", "Nature", "Substance", "Attribute", "Mode", "Ethics"]

    for i in range(min(len(dataset), 100)):
        text = dataset[i]["text"]
        if any(k in text for k in keywords):
            found_keyword = True
            break

    assert found_keyword, "Did not find expected Spinoza keywords in the dataset samples"
