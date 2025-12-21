from socials_data import load_dataset
import pytest

def test_workflow():
    # Verify we can load the data we just created
    ds_land = load_dataset("nick_land")
    assert len(ds_land) == 1
    assert "Fanged Noumena" in ds_land[0]["text"]

    ds_zizek = load_dataset("slavoj_zizek")
    assert len(ds_zizek) == 1
    assert "Ideology" in ds_zizek[0]["text"]

    ds_marcus = load_dataset("marcus_aurelius")
    assert len(ds_marcus) == 1
    assert "Stoic" in ds_marcus[0]["text"] or "meditations" in ds_marcus[0]["text"] or "grandfather" in ds_marcus[0]["text"]

    print("Workflow test passed!")

if __name__ == "__main__":
    test_workflow()
