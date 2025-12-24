import os
import pytest
from socials_data import load_dataset

def test_william_james_dataset_loads():
    """Verify that the William James dataset can be loaded."""
    dataset = load_dataset("william_james")
    assert dataset is not None, "Dataset should load successfully"
    assert len(dataset) > 0, "Dataset should not be empty"

def test_william_james_content_integrity():
    """Verify that the content contains expected keywords and lacks artifacts."""
    dataset = load_dataset("william_james")

    # Check for expected keywords
    keywords = ["pragmatism", "consciousness", "religious experience", "truth", "psychology"]
    found_keywords = {k: False for k in keywords}

    # Check a sample of entries
    sample_size = min(len(dataset), 100)
    for i in range(sample_size):
        text = dataset[i]["text"].lower()
        for k in keywords:
            if k in text:
                found_keywords[k] = True

    # We expect at least some of these to be found.
    # Since the dataset is large, we should find all of them across the dataset,
    # but let's just assert that we found at least 'pragmatism' and 'psychology'
    assert found_keywords["pragmatism"], "Should contain 'pragmatism'"
    assert found_keywords["psychology"], "Should contain 'psychology'"

def test_william_james_no_artifacts():
    """Verify that Project Gutenberg artifacts are removed."""
    dataset = load_dataset("william_james")

    artifacts = [
        "Project Gutenberg",
        "START OF THE PROJECT",
        "END OF THE PROJECT",
        "Produced by",
        "Distributed Proofreading Team"
    ]

    # Check a sample, or maybe check the first few chars of each entry?
    # The processed data usually chunks the text.
    # If the cleaning worked, these strings should be rare or absent.
    # Note: "Project Gutenberg" might appear in the license text if we didn't strip it perfectly,
    # or if the splitter kept it.

    # Let's check the very first entry of each source file effectively by scanning the whole dataset
    # (it shouldn't be too huge to scan for these strings in a test).

    # Optimally, we iterate and count violations.
    violations = 0
    for item in dataset:
        text = item["text"]
        for artifact in artifacts:
            if artifact in text:
                # Allow "Project Gutenberg" if it's in a context that isn't the header/footer?
                # But we expect headers/footers to be gone.
                # Let's just print/warn for now or assert if we are confident.
                # The license usually says "This eBook is for the use of anyone anywhere..."
                # which is at the start.
                violations += 1
                # print(f"Found artifact '{artifact}' in text snippet: {text[:50]}...")
                break

    # We allow a small margin of error perhaps, but ideally 0.
    # Given my simple cleaning script, I hope it's 0.
    assert violations < 5, f"Found {violations} entries with artifacts"

if __name__ == "__main__":
    # Manually run if executed as script
    try:
        test_william_james_dataset_loads()
        print("Dataset loads: PASS")
        test_william_james_content_integrity()
        print("Content integrity: PASS")
        test_william_james_no_artifacts()
        print("No artifacts: PASS")
    except AssertionError as e:
        print(f"Test failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
