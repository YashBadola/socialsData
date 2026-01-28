import pytest
import os
import json
from socials_data.core.loader import load_dataset

class TestLudwigWittgenstein:
    def test_load_dataset_works(self):
        """Test that the dataset can be loaded successfully."""
        dataset = load_dataset("ludwig_wittgenstein")
        assert len(dataset) > 0

    def test_dataset_content(self):
        """Test that the dataset contains expected content."""
        dataset = load_dataset("ludwig_wittgenstein")

        # Check first item structure
        item = dataset[0]
        assert "text" in item
        assert "source" in item

        # Check that we have content from different source files
        sources = set(dataset["source"])
        expected_sources = {
            "tractatus_excerpts.txt",
            "investigations_excerpts.txt"
        }

        # We should have at least some of the sources
        assert len(sources.intersection(expected_sources)) > 0

    def test_metadata_structure(self):
        """Test that the metadata is valid."""
        metadata_path = "socials_data/personalities/ludwig_wittgenstein/metadata.json"

        with open(metadata_path, 'r') as f:
            data = json.load(f)

        assert data["id"] == "ludwig_wittgenstein"
        assert data["name"] == "Ludwig Wittgenstein"
        assert "system_prompt" in data
        assert len(data["sources"]) == 2
