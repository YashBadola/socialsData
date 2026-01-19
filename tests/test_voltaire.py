import pytest
from socials_data.core.loader import load_dataset

def test_load_voltaire():
    """Test loading the Voltaire dataset."""
    dataset = load_dataset("voltaire")

    # Basic checks
    assert len(dataset) > 0
    assert "text" in dataset.features

    # Check content
    first_item = dataset[0]
    assert "CANDIDE" in first_item["text"]
