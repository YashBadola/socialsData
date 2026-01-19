from socials_data import load_dataset

try:
    dataset = load_dataset("ludwig_wittgenstein")
    print(f"Successfully loaded dataset with {len(dataset)} entries.")
    print("First entry:")
    print(dataset[0])
except Exception as e:
    print(f"Failed to load dataset: {e}")
