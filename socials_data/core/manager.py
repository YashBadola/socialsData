import json
import os
from pathlib import Path
from datasets import Dataset
import pandas as pd
from tqdm import tqdm
from .processor import DataProcessor

class PersonalityManager:
    def __init__(self, base_dir=None):
        if base_dir is None:
            # Assuming this file is in socials_data/core/
            self.base_dir = Path(__file__).parent.parent / "personalities"
        else:
            self.base_dir = Path(base_dir)

        # Ensure base directory exists
        if not self.base_dir.exists():
            self.base_dir.mkdir(parents=True, exist_ok=True)

    def list_personalities(self):
        if not self.base_dir.exists():
            return []
        return [d.name for d in self.base_dir.iterdir() if d.is_dir()]

    def add_personality(self, name):
        p_dir = self.base_dir / name
        p_dir.mkdir(exist_ok=True)
        (p_dir / "raw").mkdir(exist_ok=True)
        (p_dir / "processed").mkdir(exist_ok=True)

        metadata = {
            "name": name,
            "id": name,
            "description": "",
            "system_prompt": "",
            "sources": []
        }

        with open(p_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        return p_dir

    def get_metadata(self, name):
        p_dir = self.base_dir / name
        with open(p_dir / "metadata.json", "r") as f:
            return json.load(f)

    def process_personality(self, name, skip_qa=False):
        processor = DataProcessor(self.base_dir / name)
        processor.process_text()
        if not skip_qa:
            processor.generate_qa()

def load_dataset(name, split="train"):
    # This mimics loading the dataset using the datasets library
    # For now, we'll just load the jsonl file
    manager = PersonalityManager()
    p_dir = manager.base_dir / name
    data_file = p_dir / "processed" / "data.jsonl"

    if not data_file.exists():
        raise ValueError(f"Dataset for {name} not found or not processed.")

    return Dataset.from_json(str(data_file))
