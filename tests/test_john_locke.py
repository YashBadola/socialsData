import json
from pathlib import Path
from socials_data.core.loader import load_dataset
import pytest

def test_john_locke_metadata():
    """Test that John Locke's metadata is correct."""
    metadata_path = Path("socials_data/personalities/john_locke/metadata.json")
    assert metadata_path.exists()

    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    assert metadata["id"] == "john_locke"
    assert metadata["name"] == "John Locke"
    assert "Liberalism" in metadata["description"]
    assert "tabula rasa" in metadata["system_prompt"]
    assert len(metadata["sources"]) == 3

def test_john_locke_raw_files():
    """Test that raw files were downloaded and cleaned."""
    raw_dir = Path("socials_data/personalities/john_locke/raw")
    files = list(raw_dir.glob("*.txt"))
    assert len(files) == 3

    # Check that Gutenberg header is gone
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read(500)
            assert "*** START OF THE PROJECT GUTENBERG EBOOK" not in content
            assert "*** START OF THIS PROJECT GUTENBERG EBOOK" not in content

def test_john_locke_dataset_loading():
    """Test that the dataset can be loaded via the package loader."""
    try:
        dataset = load_dataset("john_locke")
    except Exception as e:
        pytest.fail(f"Failed to load dataset: {e}")

    assert len(dataset) > 0
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Ensure source names are correct (based on filenames)
    sources = set(dataset["source"])
    assert "second_treatise_of_government.txt" in sources
    assert "essay_concerning_human_understanding_vol1.txt" in sources
