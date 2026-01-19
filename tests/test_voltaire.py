
import pytest
import os
import json
from socials_data.core.loader import load_dataset

class TestVoltaire:
    def test_load_dataset_works(self):
        """Test that the dataset can be loaded successfully."""
        dataset = load_dataset("voltaire")
        assert len(dataset) > 0

    def test_dataset_content(self):
        """Test that the dataset contains expected content."""
        dataset = load_dataset("voltaire")

        # Check first item structure
        item = dataset[0]
        assert "text" in item
        assert "source" in item

        # Check that we have content from different source files
        sources = set(dataset["source"])
        expected_sources = {
            "candide_chap1.txt",
            "letters_on_england.txt",
            "philosophical_dictionary.txt"
        }

        # We should have all of the sources
        assert expected_sources.issubset(sources)

    def test_metadata_structure(self):
        """Test that the metadata is valid."""
        metadata_path = "socials_data/personalities/voltaire/metadata.json"

        with open(metadata_path, 'r') as f:
            data = json.load(f)

        assert data["id"] == "voltaire"
        assert data["name"] == "Voltaire"
        assert "system_prompt" in data
        assert len(data["sources"]) == 3
