from socials_data.core.loader import load_dataset
import pytest

def test_load_dataset():
    dataset = load_dataset("simone_de_beauvoir")
    assert dataset is not None
    assert len(dataset) > 0

    first_entry = dataset[0]
    assert "text" in first_entry
    assert "source" in first_entry

    # Check if we have some expected content
    text_content = [item['text'] for item in dataset]
    has_second_sex = any("The Second Sex" in item['text'] or "woman" in item['text'] for item in dataset)
    assert has_second_sex
