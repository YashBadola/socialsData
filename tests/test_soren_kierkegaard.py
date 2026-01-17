from socials_data import load_dataset
import pytest

def test_soren_kierkegaard_dataset():
    # Load dataset
    ds = load_dataset("soren_kierkegaard")
    assert len(ds) >= 3  # We have 3 files

    # Check content of one of the items
    texts = [item["text"] for item in ds]
    sources = [item["source"] for item in ds]

    # Check that we have texts from the files we added
    assert any("What is a poet?" in text for text in texts)
    assert any("The most common form of despair" in text for text in texts)
    assert any("excerpts_either_or.txt" in source for source in sources)

def test_soren_kierkegaard_metadata():
    from socials_data.core.manager import PersonalityManager
    manager = PersonalityManager()
    metadata = manager.get_metadata("soren_kierkegaard")

    assert metadata["name"] == "Søren Kierkegaard"
    assert "existentialist" in metadata["description"]
