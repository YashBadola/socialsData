import json
import pytest
from socials_data.core.loader import load_dataset
from pathlib import Path

def test_jean_jacques_rousseau_dataset():
    # Load the dataset
    dataset = load_dataset('jean_jacques_rousseau')

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check schema
    sample = dataset[0]
    assert 'text' in sample, "Dataset sample should contain 'text'"
    assert 'source' in sample, "Dataset sample should contain 'source'"

    # Verify sources
    sources = set(dataset['source'])
    expected_sources = {
        'social_contract_and_discourses.txt',
        'emile.txt',
        'confessions.txt'
    }
    assert expected_sources.issubset(sources), f"Missing sources. Found: {sources}"

    # Verify content keywords
    text_content = " ".join(dataset[:20]['text']) # Check first few chunks
    keywords = ["man", "nature", "law", "will", "contract", "education", "God"]

    found_any = False
    for keyword in keywords:
        if keyword in text_content or keyword.lower() in text_content:
            found_any = True
            break

    assert found_any, "Dataset content does not seem to contain expected keywords"

    # Verify metadata
    metadata_path = Path("socials_data/personalities/jean_jacques_rousseau/metadata.json")
    assert metadata_path.exists()

    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    assert metadata['id'] == 'jean_jacques_rousseau'
    assert metadata['name'] == 'Jean-Jacques Rousseau'
    assert "chains" in metadata['system_prompt']
