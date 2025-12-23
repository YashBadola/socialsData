import json
import pytest
from pathlib import Path
from socials_data import load_dataset
import datasets

def test_immanuel_kant_data_structure():
    base_dir = Path("socials_data/personalities/immanuel_kant")

    # Check if metadata exists
    assert (base_dir / "metadata.json").exists()

    # Check content of metadata
    with open(base_dir / "metadata.json", "r") as f:
        metadata = json.load(f)
    assert metadata["id"] == "immanuel_kant"
    assert metadata["name"] == "Immanuel Kant"
    assert "system_prompt" in metadata
    assert len(metadata["sources"]) == 4

    # Check processed data
    processed_file = base_dir / "processed" / "data.jsonl"
    assert processed_file.exists()

    with open(processed_file, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0

    # Check sample entry
    sample = json.loads(lines[0])
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

def test_immanuel_kant_load_dataset():
    # Test loading using the library function
    dataset = load_dataset("immanuel_kant")

    # The load_dataset function from socials_data might return a Dataset directly
    # if it's not a DatasetDict. Let's inspect.

    if isinstance(dataset, datasets.DatasetDict):
         assert "train" in dataset
         data = dataset["train"]
    else:
         data = dataset

    assert len(data) > 0

    # Check columns
    assert "text" in data.features
    assert "source" in data.features

    # Check content
    sample_text = data[0]["text"]
    assert isinstance(sample_text, str)

    # Check if some expected keywords appear in the dataset (rudimentary check)
    all_text = " ".join(data[:100]["text"])
    keywords = ["reason", "criticism", "judgement", "judgment", "moral", "law", "knowledge"]
    found = any(k in all_text.lower() for k in keywords)
    assert found, "Did not find expected Kantian keywords in the first 100 samples"
