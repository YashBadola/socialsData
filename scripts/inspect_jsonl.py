import json

filepath = "socials_data/personalities/bertrand_russell/processed/data.jsonl"
with open(filepath, "r") as f:
    for line in f:
        record = json.loads(line)
        source = record.get("source")
        text = record.get("text", "")
        print(f"--- Source: {source} ---")
        print(f"Start (first 200 chars):\n{text[:200]}")
        print(f"End (last 200 chars):\n{text[-200:]}")
        print("\n")
