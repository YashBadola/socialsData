import os
import json
import glob
from tqdm import tqdm

def process_personality(name, skip_qa=False):
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "personalities", name)
    if not os.path.exists(base_dir):
        print(f"Error: Personality '{name}' not found at {base_dir}")
        return

    raw_dir = os.path.join(base_dir, "raw")
    processed_dir = os.path.join(base_dir, "processed")
    os.makedirs(processed_dir, exist_ok=True)

    # Read raw files
    data_output_path = os.path.join(processed_dir, "data.jsonl")

    # Simple processing: read all text files in raw/ and write to data.jsonl
    # Note: Memories said "maps one file directly in the raw directory to one record"
    # and "does not scan subdirectories".

    raw_files = glob.glob(os.path.join(raw_dir, "*"))

    records = []
    for filepath in raw_files:
        if os.path.isfile(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        records.append({
                            "text": content,
                            "source": os.path.basename(filepath)
                        })
            except Exception as e:
                print(f"Skipping {filepath}: {e}")

    with open(data_output_path, 'w', encoding='utf-8') as f:
        for record in records:
            f.write(json.dumps(record) + "\n")

    print(f"Processed {len(records)} records to {data_output_path}")

    if not skip_qa:
        print("Q&A generation skipped (logic not fully implemented in this step).")
