
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_immanuel_kant_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "immanuel_kant" in personalities

def test_immanuel_kant_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("immanuel_kant")
    assert metadata["name"] == "Immanuel Kant"
    assert metadata["id"] == "immanuel_kant"
    assert "sources" in metadata
    assert len(metadata["sources"]) >= 3

def test_immanuel_kant_dataset_load():
    dataset = load_dataset("immanuel_kant")
    assert dataset is not None
    # We expect some data.
    # Since we sliced the texts into chunks, there should be many entries.
    assert len(dataset) > 100

    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Check if text contains some Kantian keywords
    keywords = ["reason", "critique", "metaphysic", "moral", "priori", "transcendental"]

    # We scan a few samples to find at least one keyword
    found_keyword = False
    for i in range(min(50, len(dataset))):
        text = dataset[i]["text"].lower()
        if any(k in text for k in keywords):
            found_keyword = True
            break

    assert found_keyword, "Did not find expected Kantian keywords in the first 50 samples"

if __name__ == "__main__":
    pytest.main([__file__])
