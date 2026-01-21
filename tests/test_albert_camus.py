from socials_data import load_dataset
import pytest

def test_albert_camus_load():
    ds = load_dataset("albert_camus")
    assert len(ds) > 0
    # Check that at least one item has the expected text
    texts = [item['text'] for item in ds]
    assert any("Sisyphus" in text for text in texts)

def test_albert_camus_metadata():
    import json
    with open("socials_data/personalities/albert_camus/metadata.json") as f:
        meta = json.load(f)
    assert meta['name'] == "Albert Camus"
    assert meta['id'] == "albert_camus"
