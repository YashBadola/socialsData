import json
from pathlib import Path
from socials_data.core.loader import load_dataset

def test_voltaire_dataset_exists():
    """Verify that the Voltaire dataset is reachable and has metadata."""
    manager_path = Path("socials_data/personalities/voltaire")
    assert manager_path.exists()
    assert (manager_path / "metadata.json").exists()
    assert (manager_path / "processed" / "data.jsonl").exists()

def test_voltaire_metadata_content():
    """Verify the content of metadata.json."""
    with open("socials_data/personalities/voltaire/metadata.json", "r") as f:
        metadata = json.load(f)

    assert metadata["name"] == "Voltaire"
    assert metadata["id"] == "voltaire"
    assert len(metadata["sources"]) >= 3
    assert "Candide" in [s["title"] for s in metadata["sources"]]

def test_voltaire_load_dataset():
    """Verify that load_dataset works for Voltaire."""
    dataset = load_dataset("voltaire")
    assert len(dataset) > 0
    # Check a sample
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert len(sample["text"]) > 0

def test_voltaire_content_check():
    """Check for specific keywords to ensure correct text loading."""
    dataset = load_dataset("voltaire")

    # Check for keywords from Candide
    candide_texts = [d["text"] for d in dataset if "candide.txt" in d["source"]]
    assert len(candide_texts) > 0
    # Combine texts to search (in case of chunking, though default processor might not chunk much)
    full_candide = " ".join(candide_texts).lower()
    assert "pangloss" in full_candide
    assert "cunegonde" in full_candide

    # Check for keywords from Zadig
    zadig_texts = [d["text"] for d in dataset if "zadig.txt" in d["source"]]
    assert len(zadig_texts) > 0
    full_zadig = " ".join(zadig_texts).lower()
    assert "zadig" in full_zadig
    assert "babylon" in full_zadig
