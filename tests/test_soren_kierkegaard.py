from socials_data.core.loader import load_dataset
import pytest

def test_soren_kierkegaard_dataset():
    dataset = load_dataset("soren_kierkegaard")
    assert len(dataset) > 0
    first_item = dataset[0]
    assert "text" in first_item
    assert "source" in first_item
    assert "Preface" in first_item["text"]
