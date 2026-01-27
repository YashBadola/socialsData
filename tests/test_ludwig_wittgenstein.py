from socials_data import load_dataset
import pytest

def test_ludwig_wittgenstein_dataset():
    # Load the dataset for Ludwig Wittgenstein
    dataset = load_dataset("ludwig_wittgenstein")

    # Check that we have at least one record
    assert len(dataset) > 0

    # Verify content
    text_content = dataset[0]['text']
    assert "The world is everything that is the case" in text_content
    assert "Whereof one cannot speak, thereof one must be silent" in text_content

    # Verify metadata (indirectly, if load_dataset uses it, but here we just check data)
    assert dataset[0]['source'] == 'tractatus.txt'

if __name__ == "__main__":
    test_ludwig_wittgenstein_dataset()
