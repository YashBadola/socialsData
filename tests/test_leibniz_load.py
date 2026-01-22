from socials_data import load_dataset
import sys

try:
    print("Loading dataset for gottfried_wilhelm_leibniz...")
    dataset = load_dataset("gottfried_wilhelm_leibniz")
    print(f"Loaded dataset with {len(dataset)} entries.")
    print("First entry sample:")
    print(dataset[0]['text'][:200])
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
