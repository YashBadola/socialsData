import pytest
from socials_data.core.loader import load_dataset
import os

def test_soren_kierkegaard_structure():
    base_path = "socials_data/personalities/soren_kierkegaard"
    assert os.path.exists(base_path)
    assert os.path.exists(os.path.join(base_path, "metadata.json"))
    assert os.path.exists(os.path.join(base_path, "raw"))
    assert os.path.exists(os.path.join(base_path, "processed"))
    assert os.path.exists(os.path.join(base_path, "processed", "data.jsonl"))

def test_soren_kierkegaard_content():
    dataset = load_dataset("soren_kierkegaard")
    assert len(dataset) > 0
    # Check if we have entries from both files (this is a heuristic)
    texts = [item['text'] for item in dataset]
    has_crowd = any("The Crowd is Untruth" in text for text in texts)
    has_unhappiest = any("The Unhappiest One" in text for text in texts)
    assert has_crowd, "Missing 'The Crowd is Untruth' content"
    assert has_unhappiest, "Missing 'The Unhappiest One' content"
