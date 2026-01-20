import pytest
import os
from socials_data import load_dataset

def test_simone_de_beauvoir_structure():
    base_path = "socials_data/personalities/simone_de_beauvoir"
    assert os.path.exists(os.path.join(base_path, "metadata.json"))
    assert os.path.exists(os.path.join(base_path, "raw"))
    assert os.path.exists(os.path.join(base_path, "processed"))
    assert os.path.exists(os.path.join(base_path, "processed", "data.jsonl"))

def test_load_simone_de_beauvoir_dataset():
    dataset = load_dataset("simone_de_beauvoir")
    assert len(dataset) > 0

    # Check if we have data from all sources
    sources = set(item['source'] for item in dataset)
    expected_sources = {'the_second_sex_intro.txt', 'ethics_of_ambiguity.txt', 'memoirs.txt'}
    assert expected_sources.issubset(sources)

    # Check content of a sample
    sample = next(item for item in dataset if item['source'] == 'the_second_sex_intro.txt')
    assert "One is not born, but rather becomes, a woman" in sample['text']
