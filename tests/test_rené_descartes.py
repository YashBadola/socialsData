
import pytest
from socials_data.core.loader import load_dataset

def test_load_rene_descartes_dataset():
    dataset = load_dataset('rené_descartes')
    assert len(dataset) > 0
    assert 'text' in dataset[0]
    # Check for some known text from the discourse
    found = False
    for item in dataset:
        if "COGITO ERGO SUM" in item['text']:
            found = True
            break
    assert found
