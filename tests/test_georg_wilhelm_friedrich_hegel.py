import os
import pytest
from socials_data import load_dataset

def test_load_dataset_hegel():
    ds = load_dataset("georg_wilhelm_friedrich_hegel")
    assert ds is not None
    assert len(ds) > 0

    # Check for some keywords
    found_spirit = False
    found_mind = False

    # Iterate through a few samples to verify content
    for i in range(min(100, len(ds))):
        text = ds[i]['text']
        if "Spirit" in text or "Geist" in text:
            found_spirit = True
        if "Mind" in text or "mind" in text:
            found_mind = True

    assert found_spirit, "Keyword 'Spirit' or 'Geist' not found in the first 100 samples"
    assert found_mind, "Keyword 'Mind' not found in the first 100 samples"

def test_no_gutenberg_headers():
    ds = load_dataset("georg_wilhelm_friedrich_hegel")
    for i in range(min(500, len(ds))):
        text = ds[i]['text']
        assert "START OF THE PROJECT GUTENBERG" not in text
        assert "END OF THE PROJECT GUTENBERG" not in text

if __name__ == "__main__":
    pytest.main([__file__])
