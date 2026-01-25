from socials_data import load_dataset
import pytest

def test_leibniz_dataset():
    ds = load_dataset("gottfried_wilhelm_leibniz")
    assert len(ds) > 0
    all_text = " ".join([item["text"] for item in ds])
    assert "The monad, of which we will speak here" in all_text
    assert "preestablished harmony" in all_text
