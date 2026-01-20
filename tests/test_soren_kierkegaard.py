from socials_data.core.loader import load_dataset
import pytest

def test_load_soren_kierkegaard_dataset():
    dataset = load_dataset("soren_kierkegaard")

    # Basic checks
    assert len(dataset) > 0
    assert "text" in dataset[0]

    # Check for specific content
    texts = [item["text"] for item in dataset]
    assert any("Knight of Faith" in text for text in texts)
    assert any("Anxiety may be compared with dizziness" in text for text in texts)
