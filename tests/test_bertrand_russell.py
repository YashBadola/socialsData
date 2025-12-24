import os
import pytest
from socials_data import load_dataset

def test_load_dataset_bertrand_russell():
    ds = load_dataset("bertrand_russell")
    assert len(ds) > 0

    # Check that we have the expected columns
    assert "text" in ds.column_names
    assert "source" in ds.column_names

    # Verify content from each book is present
    text_content = " ".join(ds["text"])

    # Keywords from "The Problems of Philosophy"
    assert "sense-data" in text_content
    assert "appearance and reality" in text_content.lower()

    # Keywords from "The Analysis of Mind"
    assert "mnemic causation" in text_content.lower() or "mnemic" in text_content.lower()

    # Keywords from "Mysticism and Logic"
    assert "mysticism" in text_content.lower()

    # Negative checks
    assert "Project Gutenberg" not in text_content
    assert "START OF THE PROJECT" not in text_content
