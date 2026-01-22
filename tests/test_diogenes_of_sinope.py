
import pytest
from socials_data import load_dataset
from pathlib import Path
import shutil
import os

def test_diogenes_dataset_loading():
    """
    Test that we can load the Diogenes dataset and that it contains expected data.
    """
    dataset = load_dataset("diogenes_of_sinope")

    assert len(dataset) > 0, "Dataset should not be empty"

    # Check for some characteristic content
    text_content = ""
    for item in dataset:
        text_content += item['text']

    assert "Alexander" in text_content
    assert "lamp" in text_content
    assert "citizen of the world" in text_content
