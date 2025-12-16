from socials_data import load_dataset
import pytest

def test_workflow():
    # Verify we can load the data we just created
    ds_land = load_dataset("nick_land")
    # We added new content, so now there should be 3 items
    assert len(ds_land) == 3
    # Note: dataset order might vary depending on file system or processing order.
    # We'll check if content exists in any of the items.
    all_text_land = " ".join([item["text"] for item in ds_land])
    assert "Fanged Noumena" in all_text_land
    assert "Neo-China arrives from the future" in all_text_land

    ds_zizek = load_dataset("slavoj_zizek")
    # We added new content, so now there should be 3 items
    assert len(ds_zizek) == 3
    all_text_zizek = " ".join([item["text"] for item in ds_zizek])
    assert "Ideology" in all_text_zizek
    assert "start eating that trashcan" in all_text_zizek
    assert len(ds_land) == 3
    # The order of loading might be different depending on file system, so we check existence in the whole dataset
    texts = [d["text"] for d in ds_land]
    assert any("Fanged Noumena" in t for t in texts)
    assert any("Neo-China arrives from the future" in t for t in texts)
    assert any("God does not exist" in t for t in texts)

    ds_zizek = load_dataset("slavoj_zizek")
    assert len(ds_zizek) == 3
    texts_zizek = [d["text"] for d in ds_zizek]
    assert any("Ideology" in t for t in texts_zizek)
    assert any("start eating that trashcan" in t for t in texts_zizek)
    assert any("Human Rights" in t for t in texts_zizek)

    print("Workflow test passed!")

if __name__ == "__main__":
    test_workflow()
