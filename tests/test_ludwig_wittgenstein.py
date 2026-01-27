from socials_data import load_dataset

def test_ludwig_wittgenstein():
    dataset = load_dataset("ludwig_wittgenstein")
    assert len(dataset) >= 2

    # Check for personality_id in the first record
    # Note: load_dataset might wrap things or return a HuggingFace dataset
    # If it is a HF dataset, it behaves like a list of dicts usually.
    # Let's verify what load_dataset actually returns by reading __init__.py first if I was unsure,
    # but based on previous usage in test_flow.py, it seems to be list-like.

    item = dataset[0]
    assert "personality_id" in item
    assert item["personality_id"] == "ludwig_wittgenstein"

    all_text = " ".join([item["text"] for item in dataset])

    # Tractatus
    assert "The world is all that is the case" in all_text
    assert "Whereof one cannot speak, thereof one must be silent" in all_text

    # Investigations
    assert "language-game" in all_text
    assert "beetle" in all_text

if __name__ == "__main__":
    test_ludwig_wittgenstein()
