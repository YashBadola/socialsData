import re
import json
import os

RAW_PATH = "socials_data/personalities/niccolo_machiavelli/raw/the_prince.txt"
PROCESSED_DB_PATH = "socials_data/personalities/niccolo_machiavelli/processed/machiavelli_db.json"
PROCESSED_JSONL_PATH = "socials_data/personalities/niccolo_machiavelli/processed/data.jsonl"

def main():
    if not os.path.exists(RAW_PATH):
        print(f"Error: {RAW_PATH} not found.")
        return

    with open(RAW_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Normalize newlines
    content = content.replace('\r\n', '\n')

    # Identify the start of the actual text (skip TOC and Dedication)
    # We look for the first "CHAPTER I." that is at the start of a line.
    # Note: TOC entries are indented.

    # We will split by the Chapter headers.
    # Pattern: Newline, "CHAPTER", Space, Roman Numerals, Dot, possibly some text (like footnotes), Newline
    pattern = re.compile(r'\nCHAPTER ([IVXLC]+)\..*?\n')

    parts = pattern.split(content)

    # parts[0] is everything before CHAPTER I.
    # parts[1] is "I"
    # parts[2] is text of Chapter I (including title)
    # parts[3] is "II"
    # ...

    chapters_data = []

    # We only want chapters I to XXVI.
    # The text after XXVI might contain other works (Description of methods...)
    # We need to detect where The Prince ends.
    # Chapter XXVI ends with "Edward Dacre, 1640." or similar, then "DESCRIPTION OF THE METHODS..." starts.
    # But "DESCRIPTION..." is not a CHAPTER. So it will be part of the last chunk.
    # We should truncate the last chunk.

    current_chap_idx = 1
    while current_chap_idx < len(parts):
        chap_num_roman = parts[current_chap_idx]
        chap_content = parts[current_chap_idx+1]

        # Prepare for next iteration
        current_chap_idx += 2

        # Clean content
        # The first few lines are the title.
        lines = chap_content.strip().split('\n')

        title_lines = []
        body_lines = []
        in_title = True

        for line in lines:
            line = line.strip()
            if in_title:
                if line == "":
                    # Empty line indicates end of title section
                    in_title = False
                else:
                    title_lines.append(line)
            else:
                body_lines.append(line)

        title = " ".join(title_lines)
        text = "\n".join(body_lines).strip()

        # If this is the last chapter (XXVI), we need to stop before the next work
        if chap_num_roman == "XXVI":
            # Look for "DESCRIPTION OF THE METHODS" or similar marker
            end_marker = "DESCRIPTION OF THE METHODS"
            if end_marker in text:
                text = text.split(end_marker)[0].strip()

        # Analyze topics
        topics = analyze_topics(text)

        record = {
            "chapter_number": chap_num_roman,
            "title": title,
            "text": text,
            "topics": topics,
            "source": "the_prince.txt"
        }

        chapters_data.append(record)

        # Stop if we hit XXVI (just to be safe, though loop should handle it if split worked right)
        if chap_num_roman == "XXVI":
            break

    # Save to DB
    print(f"Extracted {len(chapters_data)} chapters.")
    with open(PROCESSED_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(chapters_data, f, indent=2)

    # Save to JSONL
    with open(PROCESSED_JSONL_PATH, "w", encoding="utf-8") as f:
        for record in chapters_data:
            f.write(json.dumps(record) + "\n")

    print("Processing complete.")

KEYWORDS = [
    "virtue", "virtu", "fortune", "arms", "state", "people", "nobles",
    "cruelty", "liberality", "fox", "lion", "fear", "love", "prudence",
    "cunning", "beast", "law", "force"
]

def analyze_topics(text):
    found_topics = []
    lower_text = text.lower()
    for kw in KEYWORDS:
        # simple substring check, or word boundary? Word boundary is better.
        if re.search(r'\b' + kw + r'\b', lower_text):
            found_topics.append(kw)
    return found_topics

if __name__ == "__main__":
    main()
