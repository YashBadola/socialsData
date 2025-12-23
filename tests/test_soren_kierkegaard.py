import json
import pytest
from socials_data.core.loader import load_dataset
from pathlib import Path

def test_kierkegaard_metadata_exists():
    metadata_path = Path("socials_data/personalities/soren_kierkegaard/metadata.json")
    assert metadata_path.exists()

    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    assert metadata['id'] == 'soren_kierkegaard'
    assert metadata['name'] == 'Søren Kierkegaard'
    assert 'system_prompt' in metadata
    assert 'sources' in metadata
    assert len(metadata['sources']) > 0

def test_kierkegaard_dataset_loading():
    dataset = load_dataset('soren_kierkegaard')
    assert len(dataset) > 0

    # Check first item
    item = dataset[0]
    assert 'text' in item
    assert 'source' in item
    assert isinstance(item['text'], str)
    assert len(item['text']) > 0

    # Check for specific content we know should be there
    # "DIAPSALMATA" was the start marker, so it should be in the first chunk or early on.

    found_keyword = False
    for item in dataset:
        if "DIAPSALMATA" in item['text'] or "Either/Or" in item['text'] or "poet" in item['text']:
            found_keyword = True
            break

    assert found_keyword, "Could not find expected keywords in the dataset"

if __name__ == "__main__":
    # Manually run the test functions if executed as a script
    try:
        test_kierkegaard_metadata_exists()
        print("Metadata test passed")
        test_kierkegaard_dataset_loading()
        print("Dataset loading test passed")
    except Exception as e:
        print(f"Test failed: {e}")
        exit(1)
