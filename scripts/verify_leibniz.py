from socials_data import load_dataset

try:
    print("Loading dataset for 'gottfried_wilhelm_leibniz'...")
    dataset = load_dataset("gottfried_wilhelm_leibniz")
    print(f"Dataset loaded. Number of examples: {len(dataset)}")

    print("\n--- First Example ---")
    print(dataset[0])
    print("---------------------")

    print("\n--- Last Example ---")
    print(dataset[-1])
    print("--------------------")

except Exception as e:
    print(f"Error loading dataset: {e}")
