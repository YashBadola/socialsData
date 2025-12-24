
import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

@pytest.fixture
def personality_id():
    return "jean_jacques_rousseau"

def test_load_rousseau_dataset(personality_id):
    """Test loading the Rousseau dataset."""
    try:
        dataset = load_dataset(personality_id)
    except Exception as e:
        pytest.fail(f"Failed to load dataset for {personality_id}: {e}")

    assert dataset is not None
    assert len(dataset) > 0

    # Sample a few items to check content
    # Since dataset is not a list of dicts but a Dataset object, access columns or iterate
    # Memory says: "load_dataset returns a Hugging Face Dataset object... not split-aware... access directly"
    # Also "When slicing a Hugging Face Dataset object... it returns a dictionary of lists"

    # Determine the expected number of samples (it might be fewer than 5 if chunking is not aggressive)
    num_samples = min(5, len(dataset))
    samples = dataset[:num_samples] # this is a dict of lists
    texts = samples["text"]
    sources = samples["source"]

    assert len(texts) == num_samples
    assert len(sources) == num_samples

    for text, source in zip(texts, sources):
        assert isinstance(text, str)
        assert len(text) > 0
        assert isinstance(source, str)
        # Check source filenames match what we expect
        assert source in ["the_social_contract_and_discourses.txt", "confessions.txt", "emile.txt"]

def test_no_gutenberg_artifacts(personality_id):
    """Test that Gutenberg headers/footers are removed."""
    dataset = load_dataset(personality_id)

    # Check a random sample or all if small enough (it's large, so sample)
    # We can iterate over the whole dataset looking for artifacts if we want to be thorough,
    # but that might be slow. Let's check a reasonable number.

    # Actually, iterate all might be okay if it's just string checks on 1MB text split into chunks.
    # The chunking mechanism isn't specified but assuming reasonable chunks.

    for i in range(min(len(dataset), 1000)):
        text = dataset[i]["text"]
        assert "Project Gutenberg" not in text
        assert "*** START OF THE PROJECT GUTENBERG" not in text
        assert "END OF THE PROJECT GUTENBERG" not in text

def test_content_presence(personality_id):
    """Test that key phrases from Rousseau's works are present."""
    dataset = load_dataset(personality_id)

    found_chains = False
    found_born_free = False
    found_general_will = False

    # We need to search through the dataset
    for i in range(len(dataset)):
        text = dataset[i]["text"]
        if "chains" in text:
            found_chains = True
        if "born free" in text:
            found_born_free = True
        if "General Will" in text or "general will" in text:
            found_general_will = True

        if found_chains and found_born_free and found_general_will:
            break

    assert found_chains or found_born_free, "Expected phrases from Social Contract not found"
    assert found_general_will, "Expected phrase 'General Will' not found"
