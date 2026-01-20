from socials_data.core.loader import load_dataset
import pytest

def test_load_dataset():
    # Test loading the simone_de_beauvoir dataset
    dataset = load_dataset("simone_de_beauvoir")

    # Basic checks
    assert len(dataset) > 0
    assert "text" in dataset[0]
    assert "source" in dataset[0]

    # Check if content from one of the files is present
    found_quote = False
    for entry in dataset:
        if "One is not born, but rather becomes, a woman" in entry["text"]:
            found_quote = True
            break
    assert found_quote
