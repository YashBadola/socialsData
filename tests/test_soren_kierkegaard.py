import pytest
from socials_data.core.loader import load_dataset
import os

def test_kierkegaard_dataset_loading():
    dataset = load_dataset("søren_kierkegaard")
    assert dataset is not None
    assert len(dataset) > 0
    assert "text" in dataset[0]

def test_kierkegaard_metadata_exists():
    metadata_path = "socials_data/personalities/søren_kierkegaard/metadata.json"
    assert os.path.exists(metadata_path)

def test_kierkegaard_raw_data_exists():
    raw_path_1 = "socials_data/personalities/søren_kierkegaard/raw/fear_and_trembling_excerpt.txt"
    raw_path_2 = "socials_data/personalities/søren_kierkegaard/raw/either_or_excerpt.txt"
    assert os.path.exists(raw_path_1)
    assert os.path.exists(raw_path_2)

def test_kierkegaard_processed_data_exists():
    processed_path = "socials_data/personalities/søren_kierkegaard/processed/data.jsonl"
    assert os.path.exists(processed_path)
