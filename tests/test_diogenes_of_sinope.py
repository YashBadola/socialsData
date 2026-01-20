import pytest
from socials_data.core.loader import load_dataset
import os

def test_load_diogenes_dataset():
    """Test loading the Diogenes of Sinope dataset."""
    dataset = load_dataset("diogenes_of_sinope")

    # Check if dataset is loaded
    assert len(dataset) > 0

    # Check if expected content is present
    texts = [item['text'] for item in dataset]
    assert any("The Lantern in Daylight" in text for text in texts)
    assert any("I am looking for a human" in text for text in texts)

def test_load_diogenes_qa():
    """Test loading the Diogenes of Sinope Q&A dataset."""
    # Note: Currently load_dataset defaults to 'text' split if not specified,
    # but based on the README and code structure, we might want to verify qa existence manually
    # or if load_dataset supports split selection.

    # Let's check the file existence directly first
    qa_path = "socials_data/personalities/diogenes_of_sinope/processed/qa.jsonl"
    assert os.path.exists(qa_path)

    # If load_dataset supports loading specific files or if we can test the QA content
    import pandas as pd
    df = pd.read_json(qa_path, lines=True)
    assert not df.empty
    assert "instruction" in df.columns
    assert "response" in df.columns

    assert any("lamp" in instr for instr in df["instruction"])
