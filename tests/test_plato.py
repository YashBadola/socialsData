import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

@pytest.fixture
def manager():
    return PersonalityManager()

def test_plato_metadata_exists(manager):
    meta = manager.get_metadata("plato")
    assert meta["name"] == "Plato"
    assert meta["id"] == "plato"
    assert "The Republic" in [s["title"] for s in meta["sources"]]

def test_plato_raw_files_exist():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_path, "socials_data", "personalities", "plato", "raw")
    assert os.path.exists(os.path.join(raw_path, "the_republic.txt"))
    assert os.path.exists(os.path.join(raw_path, "symposium.txt"))
    assert os.path.exists(os.path.join(raw_path, "apology.txt"))

def test_plato_dataset_loads():
    ds = load_dataset("plato")
    assert len(ds) > 0
    sample = ds[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100
    # Check for keywords
    text_content = " ".join([d["text"] for d in ds])
    assert "Socrates" in text_content
    assert "virtue" in text_content
