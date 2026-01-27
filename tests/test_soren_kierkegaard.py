import pytest
import json
from socials_data.core.loader import load_dataset

class TestSorenKierkegaard:
    def test_load_dataset_works(self):
        """Test that the dataset can be loaded successfully."""
        dataset = load_dataset("soren_kierkegaard")
        assert len(dataset) > 0

    def test_dataset_content(self):
        """Test that the dataset contains expected content."""
        dataset = load_dataset("soren_kierkegaard")

        # Check first item structure
        item = dataset[0]
        assert "text" in item
        assert "source" in item

        # Check that we have content from different source files
        sources = set(dataset["source"])
        expected_sources = {
            "fear_and_trembling_excerpt.txt",
            "either_or_excerpt.txt",
            "sickness_unto_death_excerpt.txt"
        }

        # We should have all sources since we just processed them
        assert expected_sources.issubset(sources)

        # Check for specific text content
        all_text = " ".join([d["text"] for d in dataset])
        assert "Abraham I cannot understand" in all_text
        assert "What is a poet?" in all_text
        assert "The self is a relation" in all_text

    def test_metadata_structure(self):
        """Test that the metadata is valid."""
        metadata_path = "socials_data/personalities/soren_kierkegaard/metadata.json"

        with open(metadata_path, 'r') as f:
            data = json.load(f)

        assert data["id"] == "soren_kierkegaard"
        assert data["name"] == "Soren Kierkegaard"
        assert "system_prompt" in data
        assert len(data["sources"]) == 3
