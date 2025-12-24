
import os
import pytest
from socials_data.core.loader import load_dataset
import json

def test_bertrand_russell_load_dataset():
    # Load the dataset
    ds = load_dataset("bertrand_russell")

    # Check if dataset is not empty
    assert len(ds) > 0

    # Check if we have the expected columns
    assert "text" in ds.column_names
    assert "source" in ds.column_names

    # Check sample content from each book to ensure all were processed
    sources = set(ds["source"])
    expected_sources = {
        "problems_of_philosophy.txt",
        "analysis_of_mind.txt",
        "mysticism_and_logic.txt"
    }

    # Note: sources in processed data are filenames
    assert expected_sources.issubset(sources)

    # Check for specific text that should be present
    # Problems of Philosophy
    assert any("appearance and reality" in item["text"].lower() for item in ds)
    # Analysis of Mind
    assert any("consciousness" in item["text"].lower() for item in ds)
    # Mysticism and Logic
    assert any("mysticism" in item["text"].lower() for item in ds)

def test_metadata_integrity():
    base_path = os.path.dirname(os.path.abspath(__file__))
    metadata_path = os.path.join(base_path, "../socials_data/personalities/bertrand_russell/metadata.json")

    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    assert metadata["name"] == "Bertrand Russell"
    assert metadata["id"] == "bertrand_russell"
    assert len(metadata["sources"]) == 3
