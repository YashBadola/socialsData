from socials_data.core.loader import load_dataset
import pytest

def test_load_montaigne():
    ds = load_dataset('michel_de_montaigne')
    assert ds is not None
    assert len(ds) > 0
    assert 'text' in ds[0]
    assert "Michel de Montaigne" in ds[0]['text'] or "OF IDLENESS" in ds[0]['text']
