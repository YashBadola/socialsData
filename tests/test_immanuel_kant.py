from socials_data.core.loader import load_dataset
import pytest
from pathlib import Path

def test_immanuel_kant_loading():
    """
    Verifies that the Immanuel Kant dataset loads correctly and contains valid data.
    """
    try:
        dataset = load_dataset('immanuel_kant')
    except Exception as e:
        pytest.fail(f"Failed to load Immanuel Kant dataset: {e}")

    assert len(dataset) > 0, "Dataset should not be empty"

    # Check the first sample
    sample = dataset[0]
    assert 'text' in sample
    assert 'source' in sample
    assert sample['source'] == 'critique_of_pure_reason.txt'

    # Check content relevance
    text = sample['text'].lower()
    # "reason" or "critique" or "kant" should appear in the text somewhere given the content
    assert any(keyword in text for keyword in ['reason', 'critique', 'kant', 'transcendental', 'pure']), \
        "Text does not seem to contain expected keywords."

def test_immanuel_kant_metadata():
    """
    Verifies that the metadata is accessible and correct.
    """
    import json
    metadata_path = Path("socials_data/personalities/immanuel_kant/metadata.json")
    assert metadata_path.exists()

    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    assert metadata['id'] == 'immanuel_kant'
    assert metadata['name'] == 'Immanuel Kant'
    assert 'The Critique of Pure Reason' in [s['title'] for s in metadata['sources']]
