import pytest
from socials_data import load_dataset

def test_load_ludwig_wittgenstein():
    ds = load_dataset("ludwig_wittgenstein")
    assert len(ds) > 0
    assert "TRACTATUS LOGICO-PHILOSOPHICUS" in ds[0]["text"]
