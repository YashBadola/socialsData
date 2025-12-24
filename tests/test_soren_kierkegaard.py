import os
import pytest
from socials_data import load_dataset

def test_load_dataset_soren_kierkegaard():
    dataset = load_dataset("soren_kierkegaard")

    # Check if dataset is not empty
    assert len(dataset) > 0

    # Check one sample
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] == "selections.txt"

    # Check content keywords
    text_content = [item["text"] for item in dataset]
    combined_text = " ".join(text_content)

    assert "Kierkegaard" in combined_text or "faith" in combined_text or "anxiety" in combined_text

if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
