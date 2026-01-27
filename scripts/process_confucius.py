import re
import json
from pathlib import Path
import random

def main():
    base_dir = Path("socials_data/personalities/confucius")
    raw_file = base_dir / "raw/analects.txt"
    processed_dir = base_dir / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    data_output = processed_dir / "data.jsonl"
    qa_output = processed_dir / "qa.jsonl"

    if not raw_file.exists():
        print(f"Error: {raw_file} not found.")
        return

    with open(raw_file, "r", encoding="utf-8") as f:
        text = f.read()

    # Remove Gutenberg header/footer
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"

    if start_marker in text:
        text = text.split(start_marker)[1]
    if end_marker in text:
        text = text.split(end_marker)[0]

    # Basic cleaning
    text = text.strip()

    # Split into paragraphs
    # We treat double newlines as paragraph separators
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

    # Write data.jsonl
    with open(data_output, "w", encoding="utf-8") as f:
        for p in paragraphs:
            # Skip very short paragraphs (like page numbers or titles)
            if len(p) < 20:
                continue
            # Flatten newlines within paragraph
            clean_p = " ".join(p.split())
            record = {"text": clean_p, "source": "analects.txt"}
            f.write(json.dumps(record) + "\n")

    # Generate qa.jsonl
    qa_pairs = []

    instructions = [
        "Master, share your wisdom.",
        "What is your teaching on this?",
        "Guide me, Master.",
        "What do the ancients say?",
        "How should a superior man act?",
        "Please enlighten me.",
        "What is the path of virtue?",
        "Master, I seek your counsel."
    ]

    for p in paragraphs:
        clean_p = " ".join(p.split())

        # Look for: The Master said, '...'
        # We capture everything inside the single quotes.
        # Note: The regex needs to be greedy enough to catch the content but stop at the last quote.
        # But simple regex '([^']+)' stops at the first single quote.
        # Some quotes might contain ' (apostrophe).
        # Legge usually uses ' for quotes.

        if "The Master said," in clean_p:
            parts = clean_p.split("The Master said, '")
            if len(parts) > 1:
                # content is likely in parts[1]
                content = parts[1]
                # Try to find the closing quote.
                # Ideally it's at the end or before a citation like ' (Book X)
                # Let's assume the quote ends at the last ' of the string
                r_index = content.rfind("'")
                if r_index != -1:
                    quote = content[:r_index].strip()
                    if len(quote) > 10:
                        qa_pairs.append({
                            "instruction": random.choice(instructions),
                            "response": quote,
                            "source": "analects.txt"
                        })

    with open(qa_output, "w", encoding="utf-8") as f:
        for pair in qa_pairs:
            f.write(json.dumps(pair) + "\n")

    print(f"Processed {len(paragraphs)} paragraphs into {data_output}")
    print(f"Generated {len(qa_pairs)} QA pairs into {qa_output}")

if __name__ == "__main__":
    main()
