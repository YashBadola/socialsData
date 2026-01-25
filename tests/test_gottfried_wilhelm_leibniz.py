from socials_data import load_dataset
import pytest

def test_leibniz_load():
    ds = load_dataset("gottfried_wilhelm_leibniz")
    # We added one file, so at least one record (or exactly one depending on processing)
    assert len(ds) >= 1
    all_text = " ".join([item["text"] for item in ds])
    assert "The Monadology" in all_text
    assert "The monads have no windows" in all_text
