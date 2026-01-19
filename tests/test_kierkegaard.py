
from socials_data import load_dataset
import pytest

def test_load_kierkegaard():
    dataset = load_dataset("søren_kierkegaard")
    print(f"Loaded {len(dataset)} entries.")
    assert len(dataset) > 0
    first_entry = dataset[0]
    assert "text" in first_entry
    assert "source" in first_entry

    # Check if one of the texts contains expected string
    texts = [entry['text'] for entry in dataset]
    assert any("The self is a relation" in t for t in texts)
    assert any("Faith is precisely this paradox" in t for t in texts)

if __name__ == "__main__":
    test_load_kierkegaard()
