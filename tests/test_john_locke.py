
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_john_locke_dataset_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "john_locke" in personalities

def test_john_locke_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("john_locke")
    assert metadata["name"] == "John Locke"
    assert len(metadata["sources"]) == 3
    assert metadata["id"] == "john_locke"
    assert "tabula rasa" in metadata["system_prompt"]

def test_john_locke_dataset_content():
    dataset = load_dataset("john_locke")

    # Check if dataset is not empty
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)

    # Check sources
    sources = set(item["source"] for item in dataset)
    expected_sources = {
        "second_treatise_of_government.txt",
        "human_understanding_vol1.txt",
        "human_understanding_vol2.txt"
    }
    assert expected_sources.issubset(sources)

    # Check content relevance
    # Combine some text to search for keywords
    # dataset[:20] returns a dict of lists like {'text': [...], 'source': [...]}
    combined_text = " ".join(dataset[:20]["text"])
    keywords = ["government", "law", "nature", "understanding", "ideas", "mind"]
    assert any(keyword in combined_text.lower() for keyword in keywords)

def test_john_locke_dataset_size():
    # Ensure there are enough chunks to suggest full books were processed
    dataset = load_dataset("john_locke")
    # 3 books, ~2000 chars per chunk. These are long books.
    # Should be at least a few hundred chunks.
    assert len(dataset) > 100
