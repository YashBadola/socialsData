import os
import json
import pytest
from socials_data.core.loader import load_dataset

class TestNiccoloMachiavelli:
    @pytest.fixture
    def personality_id(self):
        return "niccolo_machiavelli"

    @pytest.fixture
    def metadata(self, personality_id):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        metadata_path = os.path.join(base_dir, "socials_data", "personalities", personality_id, "metadata.json")
        with open(metadata_path, "r") as f:
            return json.load(f)

    def test_metadata_exists_and_valid(self, metadata):
        assert metadata["id"] == "niccolo_machiavelli"
        assert metadata["name"] == "Niccolò Machiavelli"
        assert "System Prompt" not in metadata # Should be snake_case in current schema if accessed as dict? No, key is "system_prompt"
        assert "system_prompt" in metadata
        assert "virtù" in metadata["system_prompt"]
        assert len(metadata["sources"]) == 3

    def test_raw_files_exist(self, personality_id):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        raw_dir = os.path.join(base_dir, "socials_data", "personalities", personality_id, "raw")

        expected_files = [
            "the_prince.txt",
            "discourses_on_livy.txt",
            "history_of_florence.txt"
        ]

        for filename in expected_files:
            assert os.path.exists(os.path.join(raw_dir, filename))

    def test_dataset_loads(self, personality_id):
        ds = load_dataset(personality_id)
        assert len(ds) > 0

        # Check first item structure
        item = ds[0]
        assert "text" in item
        assert "source" in item
        assert isinstance(item["text"], str)

    def test_content_integrity(self, personality_id):
        ds = load_dataset(personality_id)

        # Check for keywords across a sample of texts
        all_text = " ".join([item["text"] for item in ds])

        keywords = ["Prince", "virtù", "fortune", "state", "Florence"]
        # Note: "virtù" might be anglicized or accented depending on translation, but we put it in system prompt.
        # In the text it might be "virtue" or "virtu".

        found_keywords = [kw for kw in keywords if kw.lower() in all_text.lower()]
        assert len(found_keywords) > 0

    def test_no_gutenberg_boilerplate(self, personality_id):
        ds = load_dataset(personality_id)
        all_text = " ".join([item["text"] for item in ds])

        assert "*** START OF THE PROJECT GUTENBERG" not in all_text
        assert "*** END OF THE PROJECT GUTENBERG" not in all_text
        # Check for common license phrasing that might leak
        assert "Project Gutenberg License" not in all_text[:5000] # Check start
        assert "Project Gutenberg License" not in all_text[-5000:] # Check end
