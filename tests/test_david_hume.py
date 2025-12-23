import os
import json
import pytest
from socials_data.core.manager import PersonalityManager
from datasets import load_dataset

class TestDavidHume:
    @pytest.fixture
    def manager(self):
        return PersonalityManager()

    def test_metadata_exists(self, manager):
        metadata = manager.get_metadata("david_hume")
        assert metadata["name"] == "David Hume"
        assert metadata["id"] == "david_hume"
        assert len(metadata["sources"]) == 2

    def test_processed_files_exist(self):
        base_path = "socials_data/personalities/david_hume/processed"
        assert os.path.exists(os.path.join(base_path, "data.jsonl"))

    def test_data_content(self):
        # Read the processed data directly
        data_path = "socials_data/personalities/david_hume/processed/data.jsonl"
        with open(data_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        assert len(lines) > 0

        sample = json.loads(lines[0])
        assert "text" in sample
        assert "source" in sample

        # Check if sources are correct
        sources = set()
        for line in lines:
            entry = json.loads(line)
            sources.add(entry["source"])

        assert "treatise_of_human_nature.txt" in sources
        assert "enquiry_concerning_human_understanding.txt" in sources

    def test_content_keywords(self):
        # Verify that specific content exists in the dataset
        data_path = "socials_data/personalities/david_hume/processed/data.jsonl"

        found_impression = False
        found_custom = False

        with open(data_path, "r", encoding="utf-8") as f:
            for line in f:
                entry = json.loads(line)
                text = entry["text"].lower()
                if "impression" in text:
                    found_impression = True
                if "custom" in text or "habit" in text:
                    found_custom = True
                if found_impression and found_custom:
                    break

        assert found_impression, "Should contain discussions on 'impression'"
        assert found_custom, "Should contain discussions on 'custom' or 'habit'"

if __name__ == "__main__":
    pytest.main([__file__])
