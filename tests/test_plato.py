import json
from pathlib import Path
import pytest
from socials_data.core.loader import load_dataset

def test_plato_files_exist():
    base_dir = Path("socials_data/personalities/plato")
    assert (base_dir / "metadata.json").exists()
    assert (base_dir / "raw" / "the_republic.txt").exists()
    assert (base_dir / "processed" / "data.jsonl").exists()

def test_plato_metadata():
    with open("socials_data/personalities/plato/metadata.json", "r") as f:
        metadata = json.load(f)
    assert metadata["name"] == "Plato"
    assert metadata["id"] == "plato"
    assert len(metadata["sources"]) == 4

def test_plato_dataset_loading():
    # Test loading using the package's load_dataset function
    # Note: PYTHONPATH=. is assumed when running pytest
    dataset = load_dataset("plato")
    assert len(dataset) > 0

    # Check sample content
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Check for specific keywords expected in Plato's works
    text_content = " ".join([d["text"] for d in dataset])
    assert "Socrates" in text_content
    # Check for keywords that should be present
    assert "justice" in text_content.lower() or "virtue" in text_content.lower()

    # Check that introductions are largely gone (Jowett's "Analysis" often precedes the text)
    # The start marker approach should have skipped the general "INTRODUCTION"
    # We can check the start of the Republic text in the dataset

    # Filter for republic
    republic_texts = [d["text"] for d in dataset if "republic" in d["source"]]
    if republic_texts:
        # The first chunk of republic should contain the opening line roughly
        first_chunk = republic_texts[0]
        # "I went down yesterday to the Piraeus"
        assert "I went down yesterday" in first_chunk or "Piraeus" in first_chunk

    # Filter for Apology
    apology_texts = [d["text"] for d in dataset if "apology" in d["source"]]
    if apology_texts:
        first_chunk = apology_texts[0]
        # Should start with "How you, O Athenians"
        assert "How you, O Athenians" in first_chunk

if __name__ == "__main__":
    test_plato_files_exist()
    test_plato_metadata()
    test_plato_dataset_loading()
    print("All manual checks passed.")
