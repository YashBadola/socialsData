
import pytest
import os
import json
from socials_data.core.loader import load_dataset

class TestGottfriedWilhelmLeibniz:
    def test_load_dataset_works(self):
        """Test that the dataset can be loaded successfully."""
        dataset = load_dataset("gottfried_wilhelm_leibniz")
        assert len(dataset) > 0

    def test_dataset_content(self):
        """Test that the dataset contains expected content."""
        dataset = load_dataset("gottfried_wilhelm_leibniz")

        # Check first item structure
        item = dataset[0]
        assert "text" in item
        assert "source" in item

        # Check that we have content from different source files
        sources = set(dataset["source"])
        # Note: processed/data.jsonl source field usually contains the filename from raw/
        expected_sources = {
            "monadology_excerpts.txt",
            "discourse_on_metaphysics_excerpts.txt"
        }

        # We should have all of the sources since we created them
        assert len(sources.intersection(expected_sources)) == 2

    def test_metadata_structure(self):
        """Test that the metadata is valid."""
        metadata_path = "socials_data/personalities/gottfried_wilhelm_leibniz/metadata.json"

        with open(metadata_path, 'r') as f:
            data = json.load(f)

        assert data["id"] == "gottfried_wilhelm_leibniz"
        assert data["name"] == "Gottfried Wilhelm Leibniz"
        assert "system_prompt" in data
        assert len(data["sources"]) == 2
