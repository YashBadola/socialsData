from pathlib import Path

base_path = Path(__file__).parent
metadata_path = base_path / "metadata.json"
processed_data_path = base_path / "processed" / "data.jsonl"
qa_path = base_path / "processed" / "qa.jsonl"
raw_path = base_path / "raw"
