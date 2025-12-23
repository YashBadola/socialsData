import os
import pytest
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset

class TestAristotle:
    def test_personality_exists(self):
        manager = PersonalityManager()
        personalities = manager.list_personalities()
        assert "aristotle" in personalities

    def test_metadata_correctness(self):
        manager = PersonalityManager()
        metadata = manager.get_metadata("aristotle")
        assert metadata["name"] == "Aristotle"
        assert len(metadata["sources"]) == 3
        titles = [s["title"] for s in metadata["sources"]]
        assert "The Nicomachean Ethics" in titles
        assert "Politics" in titles
        assert "Poetics" in titles

    def test_raw_files_exist(self):
        base_dir = "socials_data/personalities/aristotle/raw"
        assert os.path.exists(os.path.join(base_dir, "the_nicomachean_ethics.txt"))
        assert os.path.exists(os.path.join(base_dir, "politics.txt"))
        assert os.path.exists(os.path.join(base_dir, "poetics.txt"))

    def test_dataset_loading(self):
        dataset = load_dataset("aristotle")
        assert len(dataset) > 100  # Should be substantial

        # Check a sample
        sample = dataset[0]
        assert "text" in sample
        assert "source" in sample
        assert isinstance(sample["text"], str)
        assert len(sample["text"]) > 0

        # Check source distribution (roughly)
        sources = set(dataset["source"])
        assert "the_nicomachean_ethics.txt" in sources
        assert "politics.txt" in sources
        assert "poetics.txt" in sources

    def test_content_keywords(self):
        dataset = load_dataset("aristotle")
        # Combine some text to check for keywords
        all_text = " ".join(dataset[:100]["text"]).lower()

        # Keywords likely to appear in Aristotle's works
        keywords = ["virtue", "happiness", "state", "nature", "good"]
        found = [k for k in keywords if k in all_text]
        assert len(found) > 0
