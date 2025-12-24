import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

class TestAristotle:
    @pytest.fixture
    def manager(self):
        return PersonalityManager()

    def test_personality_exists(self, manager):
        """Verify that the aristotle personality is listed."""
        personalities = manager.list_personalities()
        assert "aristotle" in personalities

    def test_metadata(self, manager):
        """Verify that the metadata for aristotle is correct."""
        metadata = manager.get_metadata("aristotle")
        assert metadata["name"] == "Aristotle"
        assert metadata["id"] == "aristotle"
        assert "system_prompt" in metadata
        assert "Peripatetic philosopher" in metadata["system_prompt"]
        assert len(metadata["sources"]) == 3

    def test_load_dataset(self):
        """Verify that the dataset can be loaded and contains expected content."""
        dataset = load_dataset("aristotle")
        assert len(dataset) > 0

        # Check a sample
        sample = dataset[0]
        assert "text" in sample
        assert "source" in sample

        # Check for presence of key concepts from the three books
        text_content = [item["text"] for item in dataset]
        combined_text = " ".join(text_content)

        # Nicomachean Ethics
        assert "happiness" in combined_text.lower() or "virtue" in combined_text.lower()
        # Politics
        assert "state" in combined_text.lower() or "city" in combined_text.lower()
        # Poetics
        assert "tragedy" in combined_text.lower() or "imitation" in combined_text.lower()

    def test_cleanliness(self):
        """Verify that Project Gutenberg headers are removed."""
        dataset = load_dataset("aristotle")
        for item in dataset:
            text = item["text"]
            assert "*** START OF THE PROJECT GUTENBERG EBOOK" not in text
            assert "*** END OF THE PROJECT GUTENBERG EBOOK" not in text
            assert "The Project Gutenberg eBook" not in text
