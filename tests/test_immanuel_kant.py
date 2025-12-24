import os
import pytest
from socials_data.core.loader import load_dataset
from pathlib import Path
import json

def test_immanuel_kant_load_dataset():
    """Test that the Immanuel Kant dataset loads correctly."""
    dataset = load_dataset("immanuel_kant")
    assert dataset is not None
    assert len(dataset) > 0

    # Check first item
    item = dataset[0]
    assert "text" in item
    assert "source" in item
    assert isinstance(item["text"], str)
    assert len(item["text"]) > 0

def test_immanuel_kant_content_checks():
    """Test that the content is relevant to Kant and cleaned."""
    dataset = load_dataset("immanuel_kant")

    # Gather all text to search
    all_text = " ".join([d["text"] for d in dataset])

    # Check for key concepts
    assert "reason" in all_text.lower()
    assert "transcendental" in all_text.lower()

    # Negative checks (artifacts)
    # Note: "Project Gutenberg" might appear if cleaning wasn't perfect,
    # but we stripped the standard headers.
    # Let's check for the header marker itself.
    assert "*** START OF THE PROJECT GUTENBERG" not in all_text

    # Check specifically for a known line from the cleaned text
    # e.g. "We may call the faculty of cognition"
    assert "faculty of cognition" in all_text

def test_metadata():
    """Test that metadata is correct."""
    base_dir = Path(__file__).parent.parent / "socials_data" / "personalities" / "immanuel_kant"
    with open(base_dir / "metadata.json", "r") as f:
        meta = json.load(f)

    assert meta["id"] == "immanuel_kant"
    assert "sources" in meta
    assert len(meta["sources"]) == 4
    assert meta["sources"][0]["title"] == "The Critique of Pure Reason"
