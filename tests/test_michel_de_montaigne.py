
import pytest
import os
import json
from socials_data.core.loader import load_dataset

class TestMichelDeMontaigne:
    def test_load_dataset_works(self):
        """Test that the dataset can be loaded successfully."""
        dataset = load_dataset("michel_de_montaigne")
        assert len(dataset) > 0

    def test_dataset_content(self):
        """Test that the dataset contains expected content."""
        dataset = load_dataset("michel_de_montaigne")

        # Check first item structure
        item = dataset[0]
        assert "text" in item
        assert "source" in item

        # Check that we have content from the source file
        sources = set(dataset["source"])
        expected_sources = {
            "essays.txt"
        }

        # We should have the source
        assert len(sources.intersection(expected_sources)) > 0

    def test_metadata_structure(self):
        """Test that the metadata is valid."""
        metadata_path = "socials_data/personalities/michel_de_montaigne/metadata.json"

        with open(metadata_path, 'r') as f:
            data = json.load(f)

        assert data["id"] == "michel_de_montaigne"
        assert data["name"] == "Michel de Montaigne"
        assert "system_prompt" in data
        assert len(data["sources"]) == 1
