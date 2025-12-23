import os
import json
import pytest
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset

def test_immanuel_kant_dataset_structure():
    """Verify that the Immanuel Kant dataset has the correct structure and content."""

    # Check if directory exists
    base_path = "socials_data/personalities/immanuel_kant"
    assert os.path.exists(base_path)
    assert os.path.exists(os.path.join(base_path, "metadata.json"))
    assert os.path.exists(os.path.join(base_path, "raw"))
    assert os.path.exists(os.path.join(base_path, "processed", "data.jsonl"))

    # Check metadata
    with open(os.path.join(base_path, "metadata.json"), "r") as f:
        metadata = json.load(f)

    assert metadata["id"] == "immanuel_kant"
    assert metadata["name"] == "Immanuel Kant"
    assert "The Critique of Pure Reason" in [s["title"] for s in metadata["sources"]]
    assert "The Critique of Practical Reason" in [s["title"] for s in metadata["sources"]]

def test_immanuel_kant_dataset_loading():
    """Verify that the dataset can be loaded using the package's load_dataset function."""

    ds = load_dataset("immanuel_kant")

    # Check that we have a non-empty dataset
    assert len(ds) > 0

    # Check column names
    assert "text" in ds.column_names
    assert "source" in ds.column_names

    # Check content of a few samples
    # We expect keywords like "reason", "priori", "transcendental"

    found_keyword = False
    keywords = ["reason", "priori", "transcendental", "imperative", "law"]

    # Check first 20 samples
    samples = ds[:20]
    for text in samples["text"]:
        text_lower = text.lower()
        if any(k in text_lower for k in keywords):
            found_keyword = True
            break

    assert found_keyword, "Did not find expected Kantian keywords in the first 20 samples."

    # Check source attribution
    sources = set(samples["source"])
    assert any("critique_of_pure_reason.txt" in s for s in sources) or \
           any("critique_of_practical_reason.txt" in s for s in sources)
