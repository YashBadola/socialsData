from socials_data import load_dataset

def test_load_leibniz():
    try:
        ds = load_dataset("gottfried_wilhelm_leibniz")
        print(f"Successfully loaded dataset with {len(ds)} entries.")
        print("Sample entry:")
        print(ds[0]['text'][:200] + "...")
    except Exception as e:
        print(f"Failed to load dataset: {e}")
        exit(1)

if __name__ == "__main__":
    test_load_leibniz()
