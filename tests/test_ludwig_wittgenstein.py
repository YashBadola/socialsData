from socials_data import load_dataset
import pytest

def test_ludwig_wittgenstein():
    ds = load_dataset("ludwig_wittgenstein")
    assert len(ds) == 526

    # Check first item
    item0 = ds[0]
    assert item0["text"] == "The world is all that is the case."
    assert item0["proposition"] == "1"
    assert item0["german"] == "Die Welt ist alles, was der Fall ist."

    # Check another item
    # 7 Wovon man nicht sprechen kann, darüber muss man schweigen.
    last_item = ds[-1]
    assert "Whereof one cannot speak" in last_item["ogden"]
    assert "What we cannot speak about" in last_item["text"] # pmc
    assert item0["source"] == "Tractatus Logico-Philosophicus"

if __name__ == "__main__":
    test_ludwig_wittgenstein()
