import pytest
from socials_data.core.loader import load_dataset
from pathlib import Path
import json

def test_rene_descartes_exists():
    base_dir = Path("socials_data/personalities/rene_descartes")
    assert base_dir.exists()
    assert (base_dir / "metadata.json").exists()
    assert (base_dir / "raw").exists()
    assert (base_dir / "processed").exists()

def test_load_dataset_rene_descartes():
    # Test loading the dataset
    ds = load_dataset("rene_descartes")
    assert len(ds) > 0

    # Check schema
    assert "text" in ds.features
    assert "source" in ds.features

    # Check sample content
    sample = ds[0]
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100

    # Verify sources
    sources = set(ds["source"])
    assert "discourse_on_the_method.txt" in sources
    assert "six_metaphysical_meditations.txt" in sources

def test_content_keywords():
    ds = load_dataset("rene_descartes")
    text_content = " ".join(ds["text"]).lower()

    # Check for key Cartesian concepts
    assert "method" in text_content
    assert "god" in text_content
    assert "reason" in text_content
    # "cogito" might be in Latin or translated as "I think", let's check "think"
    assert "think" in text_content
