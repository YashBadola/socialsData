import json
import os
from pathlib import Path

def process_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        # Split into paragraphs based on blank lines
        # Gutenberg texts usually use double newlines for paragraph breaks
        raw_paragraphs = text.split("\n\n")

        cleaned_paragraphs = []
        for p in raw_paragraphs:
            # Unwrap lines: join lines within a paragraph with a space
            # strip() removes leading/trailing whitespace from each line
            lines = [line.strip() for line in p.splitlines() if line.strip()]
            if lines:
                cleaned_p = " ".join(lines)
                cleaned_paragraphs.append(cleaned_p)

        # Join paragraphs with double newline
        cleaned_text = "\n\n".join(cleaned_paragraphs)
        return cleaned_text
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def main():
    personality_dir = Path("socials_data/personalities/bertrand_russell")
    raw_dir = personality_dir / "raw"
    processed_dir = personality_dir / "processed"
    output_file = processed_dir / "processed/data.jsonl" # Wait, logic error in path?
    # In previous script: output_file = processed_dir / "data.jsonl"

    # Correct path
    output_file = processed_dir / "data.jsonl"

    processed_dir.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as out_f:
        if raw_dir.exists():
            for file_path in raw_dir.iterdir():
                if file_path.is_file() and file_path.suffix in ['.txt', '.md']:
                    print(f"Processing {file_path.name}...")
                    content = process_file(file_path)
                    if content:
                        record = {"text": content, "source": file_path.name}
                        out_f.write(json.dumps(record) + "\n")
    print(f"Processing complete. Data saved to {output_file}")

if __name__ == "__main__":
    main()
