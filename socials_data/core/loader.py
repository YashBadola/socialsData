from datasets import Dataset
from pathlib import Path
import os
from socials_data.core.db import DB_PATH

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
    db_uri = f"sqlite:///{DB_PATH}"
    query = "SELECT text, source FROM processed_data WHERE personality_id = :pid"

    try:
        # Dataset.from_sql returns a Dataset object directly
        # We use parameterized query to prevent SQL injection
        ds = Dataset.from_sql(query, con=db_uri, params={"pid": personality_id})

        # Split logic? Dataset.from_sql returns a single Dataset.
        # If 'split' arg is provided, the original function expected to return that split.
        # Since we only have one pile of data, we can consider it "train".

        if len(ds) == 0:
             raise FileNotFoundError(f"No processed data found for '{personality_id}'. Run 'socials-data process {personality_id}' first.")
        return ds
    except Exception as e:
        if isinstance(e, FileNotFoundError):
            raise e
        raise ValueError(f"Could not load data for {personality_id}: {e}")
