import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

class TestSigmundFreud:
    @pytest.fixture
    def personality_id(self):
        return "sigmund_freud"

    @pytest.fixture
    def manager(self):
        return PersonalityManager()

    def test_personality_exists(self, manager, personality_id):
        assert personality_id in manager.list_personalities()

    def test_metadata(self, manager, personality_id):
        metadata = manager.get_metadata(personality_id)
        assert metadata["name"] == "Sigmund Freud"
        assert "psychoanalysis" in metadata["description"].lower()
        assert "psychoanalysis" in metadata["system_prompt"].lower()

    def test_raw_files_exist(self, personality_id):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        raw_dir = os.path.join(base_dir, f"../socials_data/personalities/{personality_id}/raw")

        expected_files = [
            "the_interpretation_of_dreams.txt",
            "dream_psychology.txt",
            "three_contributions_theory_of_sex.txt",
            "psychopathology_of_everyday_life.txt"
        ]

        for file in expected_files:
            assert os.path.exists(os.path.join(raw_dir, file))

    def test_load_dataset(self, personality_id):
        ds = load_dataset(personality_id)
        assert len(ds) > 0

        # Check first sample
        sample = ds[0]
        assert "text" in sample
        assert "source" in sample
        assert isinstance(sample["text"], str)
        assert len(sample["text"]) > 0

    def test_content_check(self, personality_id):
        ds = load_dataset(personality_id)

        # Check for keywords in the dataset to ensure we have the right content
        keywords = ["dream", "unconscious", "sexual", "psychology", "neurosis"]
        found_keywords = {k: False for k in keywords}

        # Check a subset of samples to be faster
        for i in range(min(100, len(ds))):
            text = ds[i]["text"].lower()
            for k in keywords:
                if k in text:
                    found_keywords[k] = True

        # We might not find *all* keywords in the first 100 chunks, but we should find most
        assert found_keywords["dream"] or found_keywords["unconscious"]

    def test_cleanliness(self, personality_id):
        ds = load_dataset(personality_id)

        # Check for Gutenberg artifacts
        artifacts = [
            "Project Gutenberg",
            "The Project Gutenberg eBook",
            "START OF THE PROJECT",
            "END OF THE PROJECT"
        ]

        for i in range(len(ds)):
            text = ds[i]["text"]
            for artifact in artifacts:
                assert artifact not in text, f"Found artifact '{artifact}' in text chunk {i}"
