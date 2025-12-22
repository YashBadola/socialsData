import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager
from datasets import Dataset

def test_plato_dataset_structure():
    """
    Test that the Plato dataset can be loaded and has the correct structure.
    """
    # 1. Verify metadata exists
    manager = PersonalityManager()
    metadata = manager.get_metadata("plato")
    assert metadata["name"] == "Plato"
    assert metadata["id"] == "plato"
    assert len(metadata["sources"]) == 5

    # 2. Verify dataset loading
    try:
        dataset = load_dataset("plato")
    except Exception as e:
        pytest.fail(f"Failed to load dataset: {e}")

    assert isinstance(dataset, Dataset)
    assert len(dataset) > 0

    # 3. Check columns
    assert "text" in dataset.column_names
    assert "source" in dataset.column_names

    # 4. Check content sample
    sample = dataset[0]
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0
    assert sample["source"] in ["republic.txt", "apology.txt", "phaedrus.txt", "phaedo.txt", "statesman.txt"]

    # 5. Content relevance check (keyword search)
    # We expect some key Platonic terms to appear across the dataset
    all_text = " ".join(dataset["text"][:100]) # Check first 100 chunks
    keywords = ["Socrates", "virtue", "justice", "soul", "state"]
    found_keywords = [kw for kw in keywords if kw.lower() in all_text.lower()]
    assert len(found_keywords) > 0, f"None of the keywords {keywords} found in the first 100 chunks."

if __name__ == "__main__":
    test_plato_dataset_structure()
