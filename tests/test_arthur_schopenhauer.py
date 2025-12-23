
import pytest
import os
import json
from socials_data.core.loader import load_dataset

class TestArthurSchopenhauer:
    def test_load_dataset_works(self):
        """Test that the dataset can be loaded successfully."""
        dataset = load_dataset("arthur_schopenhauer")
        assert len(dataset) > 0

    def test_dataset_content(self):
        """Test that the dataset contains expected content."""
        dataset = load_dataset("arthur_schopenhauer")

        # Check first item structure
        item = dataset[0]
        assert "text" in item
        assert "source" in item

        # Check that we have content from different source files
        sources = set(dataset["source"])
        expected_sources = {
            "world_as_will_and_idea_vol1.txt",
            "studies_in_pessimism.txt",
            "art_of_literature.txt"
        }

        # We should have at least some of the sources
        assert len(sources.intersection(expected_sources)) > 0

    def test_metadata_structure(self):
        """Test that the metadata is valid."""
        metadata_path = "socials_data/personalities/arthur_schopenhauer/metadata.json"

        with open(metadata_path, 'r') as f:
            data = json.load(f)

        assert data["id"] == "arthur_schopenhauer"
        assert data["name"] == "Arthur Schopenhauer"
        assert "system_prompt" in data
        assert len(data["sources"]) == 3
