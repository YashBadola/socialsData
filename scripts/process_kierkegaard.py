import json
import os

base_dir = "socials_data/personalities/soren_kierkegaard"
raw_dir = os.path.join(base_dir, "raw")
processed_dir = os.path.join(base_dir, "processed")

data = []
for filename in sorted(os.listdir(raw_dir)):
    with open(os.path.join(raw_dir, filename), "r") as f:
        text = f.read()
    data.append({"text": text, "source": filename})

with open(os.path.join(processed_dir, "data.jsonl"), "w") as f:
    for entry in data:
        f.write(json.dumps(entry) + "\n")
