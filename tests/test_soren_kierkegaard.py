import pytest
from socials_data.core.loader import load_dataset
import os

def test_soren_kierkegaard_structure():
    base_path = "socials_data/personalities/søren_kierkegaard"
    assert os.path.exists(os.path.join(base_path, "metadata.json"))
    assert os.path.exists(os.path.join(base_path, "raw", "fear_and_trembling_excerpt.txt"))
    assert os.path.exists(os.path.join(base_path, "raw", "either_or_excerpt.txt"))
    assert os.path.exists(os.path.join(base_path, "processed", "data.jsonl"))

def test_soren_kierkegaard_load():
    dataset = load_dataset("søren_kierkegaard")
    assert len(dataset) > 0
    assert "text" in dataset[0]
    assert "source" in dataset[0]
