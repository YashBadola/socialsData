
import pytest
from socials_data.core.manager import PersonalityManager

def test_montaigne_exists():
    pm = PersonalityManager()
    personalities = pm.list_personalities()
    assert "michel_de_montaigne" in personalities

def test_montaigne_metadata():
    pm = PersonalityManager()
    metadata = pm.get_metadata("michel_de_montaigne")
    assert metadata["name"] == "Michel de Montaigne"
    assert "Essays" in metadata["sources"][0]["title"]

def test_montaigne_processed_content():
    pm = PersonalityManager()
    import json
    data_path = pm.base_dir / "michel_de_montaigne" / "processed" / "data.jsonl"
    assert data_path.exists()

    with open(data_path, "r") as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "OF IDLENESS" in first_entry["text"]
