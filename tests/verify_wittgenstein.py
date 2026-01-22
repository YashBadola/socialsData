try:
    from socials_data import load_dataset
    print("Loading dataset...")
    dataset = load_dataset("ludwig_wittgenstein")
    print(f"Dataset loaded. Size: {len(dataset)}")
    if len(dataset) > 0:
        print("First entry sample:")
        print(dataset[0]['text'][:200])
        print("...")
    else:
        print("Dataset is empty!")
        exit(1)

    # Check QA if supported, or manually check file
    import os
    qa_path = "socials_data/personalities/ludwig_wittgenstein/processed/qa.jsonl"
    if os.path.exists(qa_path):
        print(f"QA file found at {qa_path}")
        with open(qa_path, 'r') as f:
            lines = f.readlines()
            print(f"QA entries: {len(lines)}")
    else:
        print("QA file not found!")
        exit(1)

except Exception as e:
    print(f"Error: {e}")
    exit(1)
