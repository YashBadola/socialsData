import pytest
from socials_data import load_dataset
from datasets import Dataset

def test_immanuel_kant_dataset_structure():
    dataset = load_dataset('immanuel_kant')

    assert isinstance(dataset, Dataset)
    assert len(dataset) > 0
    assert 'text' in dataset.features
    assert 'source' in dataset.features

def test_immanuel_kant_content_relevance():
    dataset = load_dataset('immanuel_kant')

    # Check for keywords specific to Kant in a sample of the text
    keywords = ['reason', 'critique', 'transcendental', 'pure', 'practical', 'moral', 'imperative']

    found_keywords = 0
    sample_size = min(len(dataset), 100)

    for i in range(sample_size):
        text = dataset[i]['text'].lower()
        if any(keyword in text for keyword in keywords):
            found_keywords += 1

    # At least some chunks should contain relevant keywords
    assert found_keywords > 0, "No relevant keywords found in the first 100 samples"

def test_immanuel_kant_source_metadata():
    dataset = load_dataset('immanuel_kant')

    # Verify that sources are correctly propagated
    sources = set(dataset['source'])
    # Checking for substring match as the source field contains the filename
    assert any("critique_pure_reason" in s for s in sources) or any("critique_practical_reason" in s for s in sources)
