from socials_data import load_dataset
import sys

def verify():
    print("Loading dataset for immanuel_kant...")
    try:
        dataset = load_dataset("immanuel_kant")
        print(f"Dataset loaded. Number of entries: {len(dataset)}")

        if len(dataset) == 0:
            print("Error: Dataset is empty.")
            sys.exit(1)

        sample = dataset[0]
        print("Sample entry:")
        print(sample)

        if "text" not in sample or "source" not in sample:
            print("Error: 'text' or 'source' field missing in sample.")
            sys.exit(1)

        print("Verification successful.")
    except Exception as e:
        print(f"Verification failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify()
