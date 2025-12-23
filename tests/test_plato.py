
import pytest
import os
import json
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset
from datasets import Dataset

class TestPlato:
    @pytest.fixture
    def manager(self):
        return PersonalityManager()

    def test_plato_exists(self, manager):
        """Test that Plato is listed in the personalities."""
        personalities = manager.list_personalities()
        assert "plato" in personalities

    def test_plato_metadata(self, manager):
        """Test that Plato's metadata is correct."""
        metadata = manager.get_metadata("plato")
        assert metadata["name"] == "Plato"
        assert metadata["id"] == "plato"
        assert any(s["title"] == "The Republic" for s in metadata["sources"])

    def test_plato_dataset_loading(self):
        """Test that the Plato dataset can be loaded using load_dataset."""
        ds = load_dataset("plato")
        assert isinstance(ds, Dataset)
        assert len(ds) > 0

        # Check sample content
        sample = ds[0]
        assert "text" in sample
        assert "source" in sample
        assert isinstance(sample["text"], str)
        assert len(sample["text"]) > 0

    def test_plato_content_relevance(self):
        """Test that the content actually resembles Plato/Socrates."""
        ds = load_dataset("plato")

        # We'll check the first few samples for keywords like "Socrates", "justice", "virtue"
        # Since it's split into chunks, we might need to check a few.
        found_relevant_keyword = False
        keywords = ["Socrates", "justice", "virtue", "truth", "soul", "state", "good"]

        for i in range(min(10, len(ds))):
            text = ds[i]["text"]
            if any(k in text for k in keywords) or any(k.title() in text for k in keywords):
                found_relevant_keyword = True
                break

        assert found_relevant_keyword, "Did not find relevant keywords in the first 10 samples."

    def test_plato_raw_files_exist(self):
        """Test that raw files exist."""
        base_dir = "socials_data/personalities/plato/raw"
        assert os.path.exists(os.path.join(base_dir, "republic.txt"))
        assert os.path.exists(os.path.join(base_dir, "apology.txt"))
        assert os.path.exists(os.path.join(base_dir, "symposium.txt"))
