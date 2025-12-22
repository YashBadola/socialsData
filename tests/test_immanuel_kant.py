import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

def test_immanuel_kant_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("immanuel_kant")
    assert metadata["name"] == "Immanuel Kant"
    assert metadata["id"] == "immanuel_kant"
    assert "Critique of Pure Reason" in str(metadata["sources"])

def test_immanuel_kant_dataset_loading():
    dataset = load_dataset("immanuel_kant")
    assert len(dataset) > 0
    sample = dataset[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100

    # Check for some keywords likely to be in Kant's work
    keywords = ["reason", "metaphysics", "transcendental", "priori", "experience"]
    found_keywords = False
    for i in range(min(5, len(dataset))):
        text = dataset[i]["text"].lower()
        if any(k in text for k in keywords):
            found_keywords = True
            break

    assert found_keywords, "Did not find expected Kantian keywords in the first few samples"

if __name__ == "__main__":
    test_immanuel_kant_metadata()
    test_immanuel_kant_dataset_loading()
    print("Tests passed!")
