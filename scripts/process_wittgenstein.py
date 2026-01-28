import json
import re
from pathlib import Path

def process_tractatus():
    base_dir = Path("socials_data/personalities/ludwig_wittgenstein")
    raw_file = base_dir / "raw" / "tractatus.md"
    processed_file = base_dir / "processed" / "data.jsonl"

    # Ensure processed directory exists
    processed_file.parent.mkdir(parents=True, exist_ok=True)

    if not raw_file.exists():
        print(f"Error: {raw_file} not found.")
        return

    with open(raw_file, "r", encoding="utf-8") as f:
        content = f.readlines()

    proposition_pattern = re.compile(r"^\*\*\[([\d.]+)\]\(.*?\)\*\*\s*(.*)")

    count = 0
    with open(processed_file, "w", encoding="utf-8") as out_f:
        for line in content:
            line = line.strip()
            match = proposition_pattern.match(line)
            if match:
                prop_id = match.group(1)
                text = match.group(2)

                # Clean text: remove footnote markers like [^...]
                text = re.sub(r"\[\^.*?\]", "", text)

                record = {
                    "text": text,
                    "meta": {
                        "proposition_id": prop_id,
                        "source": "Tractatus Logico-Philosophicus"
                    }
                }
                out_f.write(json.dumps(record) + "\n")
                count += 1

    print(f"Processed {count} propositions to {processed_file}")

if __name__ == "__main__":
    process_tractatus()
