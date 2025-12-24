import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

class TestAristotle:
    def test_personality_exists(self):
        manager = PersonalityManager()
        personalities = manager.list_personalities()
        assert "aristotle" in personalities

    def test_metadata_fields(self):
        manager = PersonalityManager()
        metadata = manager.get_metadata("aristotle")
        assert metadata["name"] == "Aristotle"
        assert len(metadata["sources"]) == 3
        # Title in metadata is "The Nicomachean Ethics", so "Nicomachean Ethics" check should handle the "The"
        titles = [s["title"] for s in metadata["sources"]]
        assert any("Nicomachean Ethics" in t for t in titles)

    def test_dataset_loading(self):
        dataset = load_dataset("aristotle")
        assert len(dataset) > 0

        # Check a sample
        sample = dataset[0]
        assert "text" in sample
        assert "source" in sample
        assert isinstance(sample["text"], str)
        assert len(sample["text"]) > 0

    def test_content_verification(self):
        dataset = load_dataset("aristotle")

        # Check for keywords from the texts
        text_content = " ".join([d["text"] for d in dataset])

        # Nicomachean Ethics keywords
        assert "happiness" in text_content.lower() or "eudaimonia" in text_content.lower()
        assert "virtue" in text_content.lower()

        # Politics keywords
        assert "state" in text_content.lower() or "polis" in text_content.lower()
        assert "citizen" in text_content.lower()

        # Poetics keywords
        assert "tragedy" in text_content.lower()
        assert "imitation" in text_content.lower() or "mimesis" in text_content.lower()

    def test_cleanliness(self):
        dataset = load_dataset("aristotle")
        text_content = " ".join([d["text"] for d in dataset])

        # Ensure Gutenberg headers/footers are gone
        assert "*** START OF THE PROJECT GUTENBERG" not in text_content
        assert "*** END OF THE PROJECT GUTENBERG" not in text_content
