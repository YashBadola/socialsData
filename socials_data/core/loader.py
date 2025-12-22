from datasets import load_dataset as hf_load_dataset
from pathlib import Path
import os

PERSONALITIES_DIR = Path(__file__).parent.parent / "personalities"

def load_dataset(personality_id, split="train"):
    """
    Loads the processed dataset for a specific personality using Hugging Face datasets.

    Args:
        personality_id (str): The ID of the personality (folder name).
        split (str): The split to load (default: "train").

    Returns:
        Dataset: A Hugging Face Dataset object.
    """
    processed_path = PERSONALITIES_DIR / personality_id / "processed" / "data.jsonl"

    if not processed_path.exists():
        raise FileNotFoundError(f"Processed data not found for '{personality_id}'. Run 'socials-data process {personality_id}' first.")

    # Using 'json' script from datasets to load jsonl
    return hf_load_dataset("json", data_files=str(processed_path), split=split)
