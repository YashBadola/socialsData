import pytest
import os
import json
from socials_data.core.manager import PersonalityManager
from socials_data.core.loader import load_dataset
from datasets import Dataset

class TestDavidHume:
    @pytest.fixture
    def manager(self):
        return PersonalityManager()

    def test_metadata_exists(self, manager):
        """Test that metadata loads correctly."""
        metadata = manager.get_metadata("david_hume")
        assert metadata["name"] == "David Hume"
        assert metadata["id"] == "david_hume"
        assert len(metadata["sources"]) >= 2
        assert any(s["title"] == "A Treatise of Human Nature" for s in metadata["sources"])

    def test_processed_files_exist(self):
        """Test that processed files exist."""
        base_path = "socials_data/personalities/david_hume/processed"
        assert os.path.exists(os.path.join(base_path, "data.jsonl"))

    def test_content_verification(self):
        """Test content of the processed data."""
        data_path = "socials_data/personalities/david_hume/processed/data.jsonl"
        with open(data_path, "r") as f:
            lines = [json.loads(line) for line in f]

        assert len(lines) > 0

        # Check for specific Humean concepts
        keywords = ["custom", "impression", "idea", "cause", "effect", "skepticism", "reason", "passion"]
        found_keywords = {k: False for k in keywords}

        for entry in lines:
            text = entry["text"].lower()
            for k in keywords:
                if k in text:
                    found_keywords[k] = True

        # We expect most of these to be present in a large corpus
        assert sum(found_keywords.values()) >= len(keywords) // 2, f"Found few keywords: {found_keywords}"

    def test_load_dataset_integration(self):
        """Test integration with load_dataset."""
        ds = load_dataset("david_hume")
        assert isinstance(ds, Dataset)
        assert len(ds) > 0
        assert "text" in ds.column_names
        assert "source" in ds.column_names

        # Check sample content
        sample = ds[0]
        assert isinstance(sample["text"], str)
        assert len(sample["text"]) > 0
