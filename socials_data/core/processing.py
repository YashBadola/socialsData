import os
import json
import glob
from datasets import Dataset

def process_personality(personality_id, skip_qa=False):
    base_path = os.path.dirname(os.path.dirname(__file__))
    personality_dir = os.path.join(base_path, 'personalities', personality_id)

    if not os.path.exists(personality_dir):
        raise FileNotFoundError(f"Personality {personality_id} not found at {personality_dir}")

    raw_dir = os.path.join(personality_dir, 'raw')
    processed_dir = os.path.join(personality_dir, 'processed')
    os.makedirs(processed_dir, exist_ok=True)

    data_output_path = os.path.join(processed_dir, 'data.jsonl')

    records = []

    if os.path.exists(raw_dir):
        files = glob.glob(os.path.join(raw_dir, '*'))
        for file_path in files:
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if content.strip():
                            records.append({
                                "text": content.strip(),
                                "source": os.path.basename(file_path)
                            })
                except Exception as e:
                    print(f"Skipping file {file_path}: {e}")

    # Use Hugging Face Datasets to save, ensuring robustness and compatibility
    if records:
        ds = Dataset.from_list(records)
        ds.to_json(data_output_path, force_ascii=False)

    if not skip_qa:
        # Placeholder for Q&A generation logic if we were to implement it
        # This would use openai to generate pairs and save to qa.jsonl
        print("Q&A generation skipped (not implemented in this step).")
