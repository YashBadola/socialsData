import os
import pytest
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset

class TestHegelPersonality:
    @pytest.fixture
    def manager(self):
        return PersonalityManager()

    def test_personality_exists(self, manager):
        personalities = manager.list_personalities()
        assert "georg_wilhelm_friedrich_hegel" in personalities

    def test_metadata_structure(self, manager):
        metadata = manager.get_metadata("georg_wilhelm_friedrich_hegel")
        assert metadata["name"] == "Georg Wilhelm Friedrich Hegel"
        assert "system_prompt" in metadata
        assert "sources" in metadata
        assert len(metadata["sources"]) >= 4

    def test_raw_files_exist(self):
        base_path = os.path.join("socials_data", "personalities", "georg_wilhelm_friedrich_hegel", "raw")
        expected_files = [
            "philosophy_of_mind.txt",
            "the_logic.txt",
            "history_of_philosophy_vol1.txt",
            "history_of_philosophy_vol2.txt"
        ]
        for f in expected_files:
            assert os.path.exists(os.path.join(base_path, f))

    def test_load_dataset(self):
        dataset = load_dataset("georg_wilhelm_friedrich_hegel")
        assert len(dataset) > 0

        # Check first sample
        sample = dataset[0]
        assert "text" in sample
        assert "source" in sample
        assert isinstance(sample["text"], str)

        # Check for keywords that should be present in Hegel's work
        keywords = ["Spirit", "Mind", "Logic", "Idea", "Being", "Notion", "Absolute"]

        # Scan a few samples to find at least one keyword
        found = False
        for i in range(min(100, len(dataset))):
            text = dataset[i]["text"]
            if any(k in text for k in keywords):
                found = True
                break
        assert found, "Could not find Hegelian keywords in the first 100 samples"

    def test_no_gutenberg_header(self):
        dataset = load_dataset("georg_wilhelm_friedrich_hegel")
        # Check the first few samples to ensure clean start
        for i in range(min(5, len(dataset))):
            text = dataset[i]["text"]
            assert "START OF THE PROJECT GUTENBERG" not in text
            assert "Project Gutenberg License" not in text[:500]  # License might be mentioned in body but not as header
