from socials_data.core.loader import load_dataset
import pytest

def test_heraclitus_dataset_loading():
    dataset = load_dataset("heraclitus")
    assert len(dataset) > 0
    assert "text" in dataset[0]
    assert "source" in dataset[0]

    # Verify some content
    texts = [item["text"] for item in dataset]
    assert any("rivers" in text for text in texts)
    assert any("Fire" in text for text in texts)
    assert any("Logos" in text for text in texts)

def test_heraclitus_metadata():
    import json
    from pathlib import Path

    metadata_path = Path("socials_data/personalities/heraclitus/metadata.json")
    assert metadata_path.exists()

    with open(metadata_path, "r") as f:
        meta = json.load(f)

    assert meta["id"] == "heraclitus"
    assert "Flux" in meta["system_prompt"] or "flux" in meta["system_prompt"]
