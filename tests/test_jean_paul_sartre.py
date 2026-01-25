import pytest
import os
import json
from socials_data.core.loader import load_dataset

class TestJeanPaulSartre:
    def test_load_dataset_works(self):
        """Test that the dataset can be loaded successfully."""
        dataset = load_dataset("jean_paul_sartre")
        assert len(dataset) > 0

    def test_dataset_content(self):
        """Test that the dataset contains expected content."""
        dataset = load_dataset("jean_paul_sartre")

        # Check first item structure
        item = dataset[0]
        assert "text" in item
        assert "source" in item

        # Check that we have content from different source files
        sources = set(dataset["source"])
        expected_sources = {
            "01_introduction.txt",
            "04_anguish_abandonment_despair.txt",
            "08_conclusion.txt"
        }

        # We should have intersection
        assert len(sources.intersection(expected_sources)) > 0

    def test_metadata_structure(self):
        """Test that the metadata is valid."""
        metadata_path = "socials_data/personalities/jean_paul_sartre/metadata.json"

        with open(metadata_path, 'r') as f:
            data = json.load(f)

        assert data["id"] == "jean_paul_sartre"
        assert data["name"] == "Jean-Paul Sartre"
        assert "system_prompt" in data
        assert len(data["sources"]) >= 1
