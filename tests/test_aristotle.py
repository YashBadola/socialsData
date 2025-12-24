import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

class TestAristotle:
    def setup_method(self):
        self.personality_id = "aristotle"
        self.manager = PersonalityManager()

    def test_personality_exists(self):
        """Test that the personality is listed by the manager."""
        personalities = self.manager.list_personalities()
        assert self.personality_id in personalities

    def test_metadata_structure(self):
        """Test that metadata contains required fields."""
        metadata = self.manager.get_metadata(self.personality_id)
        assert metadata["name"] == "Aristotle"
        assert "system_prompt" in metadata
        assert "sources" in metadata
        assert len(metadata["sources"]) == 4

    def test_dataset_loading(self):
        """Test that the dataset loads correctly using the loader."""
        try:
            dataset = load_dataset(self.personality_id)
            assert len(dataset) > 0

            # Check a sample
            sample = dataset[0]
            assert "text" in sample
            assert "source" in sample
            assert isinstance(sample["text"], str)

            # Check for relevant keywords in the dataset to ensure content quality
            # We'll check the first few rows for keywords related to Aristotle
            found_keyword = False
            keywords = ["virtue", "political", "tragedy", "substance", "good", "state", "poetry", "imitation"]

            for i in range(min(10, len(dataset))):
                text = dataset[i]["text"].lower()
                if any(k in text for k in keywords):
                    found_keyword = True
                    break

            assert found_keyword, "Did not find expected keywords in the first 10 samples"

        except Exception as e:
            pytest.fail(f"Failed to load dataset: {e}")

    def test_raw_files_cleaned(self):
        """Test that raw files don't have Gutenberg headers."""
        raw_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../socials_data/personalities/aristotle/raw")

        # We check the processed file indirectly via the dataset, but let's check one raw file manually
        # to ensure the cleaning script worked.

        # Note: In a real test environment we might not want to rely on file paths this way if testing against a package,
        # but here we are in the repo.

        if os.path.exists(raw_dir):
            for filename in os.listdir(raw_dir):
                if filename.endswith(".txt"):
                    with open(os.path.join(raw_dir, filename), "r", encoding="utf-8") as f:
                        content = f.read(1000) # Read start
                        assert "START OF THE PROJECT GUTENBERG" not in content

                    with open(os.path.join(raw_dir, filename), "r", encoding="utf-8") as f:
                        # Go to end
                        f.seek(0, 2)
                        size = f.tell()
                        f.seek(max(0, size - 1000), 0)
                        content = f.read()
                        assert "END OF THE PROJECT GUTENBERG" not in content
