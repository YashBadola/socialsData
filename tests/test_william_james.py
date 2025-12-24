import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

class TestWilliamJames:
    def setup_method(self):
        self.personality_id = "william_james"
        self.manager = PersonalityManager()

    def test_personality_exists(self):
        """Test that the personality is correctly registered and metadata is loadable."""
        metadata = self.manager.get_metadata(self.personality_id)
        assert metadata["id"] == self.personality_id
        assert metadata["name"] == "William James"
        assert len(metadata["sources"]) == 4

    def test_raw_files_exist(self):
        """Test that raw files were downloaded."""
        raw_dir = os.path.join("socials_data", "personalities", self.personality_id, "raw")
        assert os.path.exists(os.path.join(raw_dir, "varieties_of_religious_experience.txt"))
        assert os.path.exists(os.path.join(raw_dir, "pragmatism.txt"))
        assert os.path.exists(os.path.join(raw_dir, "meaning_of_truth.txt"))
        assert os.path.exists(os.path.join(raw_dir, "essays_in_radical_empiricism.txt"))

    def test_load_dataset(self):
        """Test that the dataset loads using the loader."""
        dataset = load_dataset(self.personality_id)
        assert len(dataset) > 0
        sample = dataset[0]
        assert "text" in sample
        assert "source" in sample
        # Check for content that should be in William James's works
        # "Pragmatism" or "religious" or "truth"

        # We can also check if we successfully stripped the header in the first chunk
        # Note: The first chunk might not be the start of the book if chunking is random or strict,
        # but usually it's sequential.
        # Let's check that we don't see "START OF THE PROJECT GUTENBERG" in any text.

        for item in dataset:
            assert "START OF THE PROJECT GUTENBERG" not in item["text"]
            assert "END OF THE PROJECT GUTENBERG" not in item["text"]
            assert "Project Gutenberg License" not in item["text"]
