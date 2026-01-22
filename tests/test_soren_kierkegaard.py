import pytest
from socials_data.core.manager import PersonalityManager
import json

@pytest.fixture
def manager():
    return PersonalityManager()

def test_soren_kierkegaard_exists(manager):
    personalities = manager.list_personalities()
    assert "soren_kierkegaard" in personalities

def test_soren_kierkegaard_metadata(manager):
    metadata = manager.get_metadata("soren_kierkegaard")
    assert metadata["name"] == "Søren Kierkegaard"
    assert "existentialist" in metadata["description"].lower()

def test_soren_kierkegaard_processed_data(manager):
    data_path = manager.base_dir / "soren_kierkegaard" / "processed" / "data.jsonl"
    assert data_path.exists()

    with open(data_path, "r") as f:
        lines = f.readlines()
        assert len(lines) > 0

        data = json.loads(lines[0])
        assert "text" in data
        assert "source" in data
