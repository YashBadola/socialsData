from datasets import load_dataset as hf_load_dataset
from pathlib import Path
import os

PERSONALITIES_DIR = Path(__file__).parent.parent / "personalities"

def load_dataset(personality_id, split="train", data_type="text"):
    """
    Loads the processed dataset for a specific personality using Hugging Face datasets.

    Args:
        personality_id (str): The ID of the personality (folder name).
        split (str): The split to load (default: "train").
        data_type (str): The type of data to load ("text" or "qa"). Defaults to "text".

    Returns:
        Dataset: A Hugging Face Dataset object.
    """
    filename = "qa.jsonl" if data_type == "qa" else "data.jsonl"
    processed_path = PERSONALITIES_DIR / personality_id / "processed" / filename

    if not processed_path.exists():
        raise FileNotFoundError(f"Processed {data_type} data not found for '{personality_id}'. Run 'socials-data process {personality_id}' first.")

    # Using 'json' script from datasets to load jsonl
    return hf_load_dataset("json", data_files=str(processed_path), split=split)
