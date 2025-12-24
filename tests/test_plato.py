import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

PERSONALITY_ID = "plato"

def test_plato_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert PERSONALITY_ID in personalities

def test_plato_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata(PERSONALITY_ID)
    assert metadata["name"] == "Plato"
    assert len(metadata["sources"]) >= 4
    assert metadata["id"] == PERSONALITY_ID

def test_plato_load_dataset():
    # This assumes the dataset has been processed
    try:
        dataset = load_dataset(PERSONALITY_ID)
        assert dataset is not None
        assert len(dataset) > 0

        # Check a sample
        sample = dataset[0]
        assert "text" in sample
        assert "source" in sample

        # Basic content check
        text_content = " ".join([d["text"] for d in dataset])
        # Keywords we expect in Plato's works
        assert "Socrates" in text_content
        assert "justice" in text_content or "virtue" in text_content

    except FileNotFoundError:
        pytest.fail(f"Dataset for {PERSONALITY_ID} not found. Did you run 'process'?")

def test_plato_raw_files_cleaned():
    # Verify that Gutenberg headers are gone from at least one file
    raw_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../socials_data/personalities/{PERSONALITY_ID}/raw")
    republic_path = os.path.join(raw_dir, "the_republic.txt")

    if os.path.exists(republic_path):
        with open(republic_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "*** START OF THE PROJECT GUTENBERG EBOOK" not in content
            assert "*** END OF THE PROJECT GUTENBERG EBOOK" not in content
