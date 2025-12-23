import json
from pathlib import Path
from socials_data.core.loader import load_dataset

def test_immanuel_kant_dataset():
    # 1. Test Metadata
    metadata_path = Path("socials_data/personalities/immanuel_kant/metadata.json")
    assert metadata_path.exists()
    with open(metadata_path, "r") as f:
        metadata = json.load(f)
    assert metadata["name"] == "Immanuel Kant"
    assert metadata["id"] == "immanuel_kant"
    assert len(metadata["sources"]) == 3

    # 2. Test Processed Data loading
    # The load_dataset function loads the dataset using the datasets library
    dataset = load_dataset("immanuel_kant")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # 3. Check specific content to ensure correct files were processed
    # Look for keywords from the processed text
    combined_text = "".join(dataset[:100]["text"])
    assert "reason" in combined_text.lower() or "critique" in combined_text.lower()

    # Check source filenames
    sources = set(dataset[:]["source"])
    expected_sources = {
        "critique_of_pure_reason.txt",
        "critique_of_practical_reason.txt",
        "critique_of_judgement.txt"
    }
    # It's possible not all files end up in the first chunk if they are large,
    # but with 'dataset[:]' we get all.
    # Note: dataset[:] returns a dictionary of lists.

    # We verify at least some of the expected sources are present.
    # (Depending on splitting, maybe not all are guaranteed if we just check a subset,
    # but dataset[:] checks all).
    found_sources = set(dataset[:]["source"])
    assert len(found_sources.intersection(expected_sources)) > 0
