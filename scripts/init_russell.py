import os
import json
import re
import urllib.request
from pathlib import Path
import sys

# Ensure we can import from the source tree
sys.path.insert(0, os.getcwd())

from socials_data.core.manager import PersonalityManager
from socials_data.core.processor import TextDataProcessor

def clean_gutenberg_text(content):
    # Patterns to identify start and end of Gutenberg text
    start_patterns = [
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
    ]
    end_patterns = [
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
    ]

    start_idx = 0
    for pattern in start_patterns:
        match = re.search(pattern, content)
        if match:
            start_idx = match.end()
            break

    end_idx = len(content)
    for pattern in end_patterns:
        match = re.search(pattern, content)
        if match:
            end_idx = match.start()
            break

    # Clean text
    return content[start_idx:end_idx].strip()

def main():
    print("Initializing PersonalityManager...")
    manager = PersonalityManager()

    name = "Bertrand Russell"
    try:
        pid = manager.create_personality(name)
        print(f"Created personality '{name}' with ID '{pid}'")
    except FileExistsError:
        pid = "bertrand_russell"
        print(f"Personality '{pid}' already exists.")

    personality_dir = manager.base_dir / pid

    # Update metadata
    metadata_path = personality_dir / "metadata.json"
    with open(metadata_path, "r") as f:
        meta = json.load(f)

    meta["description"] = "British mathematician, philosopher, logician, and public intellectual."
    meta["sources"].append({
        "type": "book",
        "title": "The Problems of Philosophy",
        "url": "https://www.gutenberg.org/cache/epub/5827/pg5827.txt"
    })

    with open(metadata_path, "w") as f:
        json.dump(meta, f, indent=2)

    print("Downloading 'The Problems of Philosophy'...")
    url = "https://www.gutenberg.org/cache/epub/5827/pg5827.txt"
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error downloading file: {e}")
        return

    print("Cleaning text...")
    cleaned_text = clean_gutenberg_text(content)

    raw_path = personality_dir / "raw" / "the_problems_of_philosophy.txt"
    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(cleaned_text)
    print(f"Saved cleaned text to {raw_path}")

    print("Processing data...")
    processor = TextDataProcessor()
    processor.process(personality_dir, skip_qa=True)
    print(f"Data processed and saved to {personality_dir}/processed/data.jsonl")

if __name__ == "__main__":
    main()
