import pytest
from socials_data.core.loader import load_dataset
import os

def test_load_simone_de_beauvoir_data():
    """Test loading the Simone de Beauvoir dataset."""
    try:
        dataset = load_dataset("simone_de_beauvoir")
    except ValueError as e:
        pytest.fail(f"Failed to load dataset: {e}")

    assert dataset is not None
    assert len(dataset) > 0

    # Check if the text content matches one of our expected sources
    texts = [item['text'] for item in dataset]
    sources = [item['source'] for item in dataset]

    assert any("The Second Sex" in source or "the_second_sex" in source for source in sources)
    assert any("Ethics of Ambiguity" in source or "ethics_of_ambiguity" in source for source in sources)
    assert any("Memoirs" in source or "memoirs" in source for source in sources)
