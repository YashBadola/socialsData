import pytest
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset

class TestAristotle:
    @pytest.fixture
    def manager(self):
        return PersonalityManager()

    def test_personality_exists(self, manager):
        personalities = manager.list_personalities()
        assert "aristotle" in personalities

    def test_metadata_structure(self, manager):
        metadata = manager.get_metadata("aristotle")
        assert metadata["name"] == "Aristotle"
        assert "system_prompt" in metadata
        assert len(metadata["sources"]) == 4
        assert metadata["sources"][0]["title"] == "The Nicomachean Ethics"
        assert metadata["sources"][3]["title"] == "The Athenian Constitution"

    def test_dataset_loading(self):
        dataset = load_dataset("aristotle")
        assert len(dataset) > 0

        # Check first sample
        sample = dataset[0]
        assert "text" in sample
        assert "source" in sample
        assert isinstance(sample["text"], str)
        assert len(sample["text"]) > 0

    def test_content_relevance(self):
        dataset = load_dataset("aristotle")
        # Check for some Aristotelian keywords in the first few samples
        text_content = " ".join([d["text"] for d in dataset.select(range(min(10, len(dataset))))])
        keywords = ["virtue", "politics", "nature", "cause", "man", "good", "state"]

        # At least one keyword should be present
        found = any(keyword in text_content.lower() for keyword in keywords)
        assert found, f"None of the keywords {keywords} found in the sample text."
