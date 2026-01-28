from socials_data.core.loader import load_dataset

def test_aristotle_load():
    ds = load_dataset("aristotle")
    assert len(ds) > 0
    assert "text" in ds[0]
