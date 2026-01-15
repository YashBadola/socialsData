import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager
from pathlib import Path
import shutil

@pytest.fixture
def kierkegaard_setup():
    manager = PersonalityManager()
    personality_dir = manager.base_dir / "søren_kierkegaard"

    # Ensure it exists (it should, based on my previous steps)
    if not personality_dir.exists():
        pytest.fail("Søren Kierkegaard personality not found. Did you run 'socials-data add'?")

    yield personality_dir

    # Cleanup if needed? No, we probably want to keep it for manual inspection.
    # But for a pure test, we might want to ensure state.
    # For now, I'll just yield.

def test_kierkegaard_processing(kierkegaard_setup):
    """Test that the Søren Kierkegaard dataset loads correctly."""

    # We assume 'socials-data process' has been run.
    # If not, we can run it here programmatically, but the plan was to run it via CLI.
    # Let's verify the output file exists.

    processed_file = kierkegaard_setup / "processed" / "data.jsonl"
    assert processed_file.exists()

    # Check content
    dataset = load_dataset("søren_kierkegaard")
    assert len(dataset) > 0

    # Check for specific text
    texts = [item['text'] for item in dataset]
    assert any("The Sickness Unto Death is despair." in t for t in texts)
    assert any("Knight of Faith" in t for t in texts)
    assert any("Either/Or" in t for t in texts)

def test_kierkegaard_metadata(kierkegaard_setup):
    manager = PersonalityManager()
    meta = manager.get_metadata("søren_kierkegaard")

    assert meta['name'] == "Søren Kierkegaard"
    assert "existentialist" in meta['description']
    assert len(meta['sources']) >= 3
