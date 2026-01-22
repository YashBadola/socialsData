import json
import re
import sys
import os

def clean_simone(filepath, output_path):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Find the separator line which is usually before the actual text starts (after the TOC)
    separator = "__________________________________________________________________"
    parts = text.split(separator)

    if len(parts) >= 2:
        # The text we want is in the second part
        text = parts[1]

    # Now find the end.
    end_marker = "Table of Contents"
    end_pos = text.rfind(end_marker) # Search from right to find the footer TOC link

    if end_pos != -1:
        text = text[:end_pos]

    # Remove [n] markers
    text = re.sub(r'\[\d+\]', '', text)

    # Remove the [n] from the start of lines if any remains
    text = re.sub(r'^\s*\[\d+\]', '', text, flags=re.MULTILINE)

    # Split into paragraphs
    paragraphs = text.split('\n\n')

    cleaned_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith("http") and len(p) > 50:
             # Clean up internal newlines and whitespace
             p = p.replace('\n', ' ')
             p = re.sub(r'\s+', ' ', p)
             cleaned_paragraphs.append(p)

    # Write to JSONL
    with open(output_path, 'w', encoding='utf-8') as f:
        for p in cleaned_paragraphs:
            entry = {
                "text": p,
                "source": "the_ethics_of_ambiguity.txt"
            }
            f.write(json.dumps(entry) + '\n')

    print(f"Processed {len(cleaned_paragraphs)} paragraphs to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/clean_simone.py <input_file> <output_file>")
        sys.exit(1)

    clean_simone(sys.argv[1], sys.argv[2])
