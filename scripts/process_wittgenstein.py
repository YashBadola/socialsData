import re
import json
import os

def process_tractatus():
    raw_path = "socials_data/personalities/ludwig_wittgenstein/raw/tractatus.txt"
    processed_path = "socials_data/personalities/ludwig_wittgenstein/processed/data.jsonl"

    if not os.path.exists(raw_path):
        print(f"Error: {raw_path} not found.")
        return

    with open(raw_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Remove Gutenberg Header/Footer
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK, TRACTATUS LOGICO-PHILOSOPHICUS ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK, TRACTATUS LOGICO-PHILOSOPHICUS ***"

    start_idx = content.find(start_marker)
    if start_idx != -1:
        content = content[start_idx + len(start_marker):]

    end_idx = content.find(end_marker)
    if end_idx != -1:
        content = content[:end_idx]

    # 2. Parse Propositions
    # Split by double newlines to identify paragraphs
    paragraphs = re.split(r'\n\s*\n', content)

    propositions = []

    # Pattern: Start of string, Digits, (dot Digits)*, Space
    prop_pattern = re.compile(r'^(\d+(?:\.\d+)*)\s+(.*)', re.DOTALL)

    for p in paragraphs:
        p = p.strip()
        if not p:
            continue

        match = prop_pattern.match(p)
        if match:
            prop_id = match.group(1)
            text = match.group(2)
            # Clean up newlines within the text
            text = " ".join(text.split())

            propositions.append({
                "text": text,
                "proposition_id": prop_id,
                "source": "Tractatus Logico-Philosophicus"
            })

    # 3. Write to JSONL
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    with open(processed_path, "w", encoding="utf-8") as f:
        for prop in propositions:
            f.write(json.dumps(prop) + "\n")

    print(f"Processed {len(propositions)} propositions.")

if __name__ == "__main__":
    process_tractatus()
